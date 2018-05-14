#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from exitstatus import ExitStatus
# deviating from standard style to remove circular dependency problem.
import webbreaker.webinspect.common.helper
from webbreaker.webinspect.authentication import WebInspectAuth
from webbreaker.common.confighelper import Config

from webbreaker.common.webbreakerlogger import Logger


from multiprocessing.dummy import Pool as ThreadPool
try:  # python 3
    import queue
except ImportError:  # python 2
    import Queue as queue


class WebInspectJitScheduler(object):
    def __init__(self, endpoints, server_size_needed, username=None, password=None, timeout=60):
        """
        The Just-In-Time Scheduler is meant to take in a list of endpoints (either passed in from a user or from a
            config) and return one that is not busy running scans.

            The servers are designed to be two different sizes and the user is allowed to choose if they want a large
            medium, or small server (default is large).

            JIT filters the list of endpoints for servers of that size and makes an api call to that server for it's
            running scans. It does this multi-threaded so whoever responds back quickest wins.

            It will timeout if no server responds back within 30 seconds - though this number is arbitrary right now.

        :param endpoints: different possible endpoints to use to scan, is a list of [['url', size], ... ]
        :param server_size_needed: size of server you want to run a scan on, passed from a cli
        :param username:
        :param password:
        """
        self.endpoints = endpoints

        auth_config = WebInspectAuth()
        self.username, self.password = auth_config.authenticate(username, password)

        self.server_size_needed = self._convert_server_size_needed_to_int(server_size_needed)
        print("server_size_need ", self.server_size_needed)

        Logger.app.debug("endpoints: {}".format(self.endpoints))
        Logger.app.debug("username: {}".format(self.username))

        Logger.app.debug("server_size_needed: {}".format(self.server_size_needed))

        # used for multi threading the _is_available API call
        # self._results_queue = queue.Queue()
        # self.timeout = timeout

    def get_endpoint(self):
        """
        public method for finding an endpoint that is: the size required, not at max capacity
        :return: an endpoint that you can run webinspect commands on. None if no available endpoints
        """

        # TODO revert, no multithreading
        try:
            endpoint = self._get_available_endpoint()
            print("***********", endpoint)
            if endpoint:
                Logger.app.info("WebBreaker has selected {} as a server for your WebInspect scan".format(endpoint[0]))
            else:
                Logger.app.error("There are no avaiable WebInspect servers")
            return endpoint[0]
        except NoServersAvailableError:
            Logger.app.error("No Server available error")
            return None

    def _get_available_endpoint(self):
        """
        Private method that handles filtering endpoints of the right size, parallely asking those endpoints if they're
        available and handling what they find out.
        :return: an endpoint that a scan can be ran on or raise a NoServersAvailableError
        """
        Logger.app.debug("Searching for appropriately sized servers")

        correct_sized_endpoints = self._get_endpoints_of_the_right_size()
        # print("^^^^^correct size ", correct_sized_endpoints)
        Logger.app.debug("correct_sized_endpoints: {}".format(correct_sized_endpoints))

        # TODO REVERT
        for endpoint in correct_sized_endpoints:
            print("***get available endpoint: ", correct_sized_endpoints)
            if self._is_endpoint_available(webinspect_endpoint=endpoint):
                # print("Im here")
                Logger.app.info("Endpoint found: {}".format(endpoint))
                return endpoint
        return None

    # TODO TODO TODO not getting the right size
    def _get_endpoints_of_the_right_size(self):
        """
        Given the provided max_concurrent_scans value, return a list of endpoints that are capable of running
        exactly than many scans. This does NOT take into consideration how many scans are currently running,
        it's just to determine if it's possible.
        :return: return all endpoints that are the size required
        """
        possible_endpoints = []
        print("****get endpoints of right size ", possible_endpoints)
        for endpoint in self.endpoints:

            # endpoint[1] is either 1 or 2 aka max concurrent scans - it's also a string so need to cast as int.
            try:  # verify endpoint[1] is a int
                print("---endpoint[1]---", int(endpoint[1]))
                if int(endpoint[1]) == self.server_size_needed:
                    append = possible_endpoints.append(endpoint)
                    print("---append--", append)

            except ValueError as e:
                Logger.app.error("There was a problem with the config.ini server|endpoint: {}".format(e))
        print("---return possible endpoints---", possible_endpoints)
        return possible_endpoints

    def _is_endpoint_available(self, webinspect_endpoint):
        """
        Determine if the provided endpoint is available. (i.e. are there less than max_concurrent_scans
        with a Status of Running on the endpoints
        :param endpoint: The endpoint to evaluate
        :param max_concurrent_scans:  The max number of allowed scans to be running on the endpoint
        """

        # Doing it kind of ugly - it removes a circular dependency issue, it's functionally the same as other uses of
        #  WebInspectAPIHelper.
        api = webbreaker.webinspect.common.helper.WebInspectAPIHelper(host=webinspect_endpoint[0], username=self.username, password=self.password, silent=True)

        # list_running_scans is in version 1.0.31 webinspectapi
        response = api.list_running_scans()
        # print("endpoint 1 ", webinspect_endpoint[1])
        active_scan = 0
        if response.success:
            for scan in response.data:
                if scan["Status"] == 'Running':
                    active_scan += 1
            if active_scan < int(webinspect_endpoint[1]):
                return True

        return False

    @staticmethod
    def _convert_server_size_needed_to_int(server_size_needed):
        """
        converts the cli large/medium/small into the value set in the config for a [large|medium|small]_server_max_concurrent_scans
            by default this is large = 2, medium = 1, small = 1 but can be changed.
        :param server_size_needed:
        :return:
        """
        # default is large.
        try:  # if value in config is not an integer will fail.
            if server_size_needed.lower() in ['large']:
                Logger.app.info("A large server will be selected to handle this request.")
                large_server_max_concurrent_scans = Config().conf_get('webinspect', 'large_server_max_concurrent_scans')
                return int(large_server_max_concurrent_scans)  # by default 2

            # medium exists for some backwards compatibility.
            if server_size_needed.lower() in ['medium']:

                Logger.app.info("A medium server will be selected to handle this request.")
                medium_server_max_concurrent_scans = Config().conf_get('webinspect', 'medium_server_max_concurrent_scans')
                return int(medium_server_max_concurrent_scans)  # by default 1

            if server_size_needed.lower() in ['small']:
                Logger.app.info("A small server will be selected to handle this request.")
                small_server_max_concurrent_scans = Config().conf_get('webinspect', 'small_server_max_concurrent_scans')
                return int(small_server_max_concurrent_scans)  # by default 1
            else:
                Logger.app.error("Size doesn't exist! Valid sizes are 'small' or 'large' or 'medium'")
                sys.exit(ExitStatus.failure)
        except TypeError as e:
            Logger.app.error("value in config for [large/medium/small]_server_max_concurrent_scans is not an integer. "
                             "{}".format(e))
            sys.exit(ExitStatus.failure)


class NoServersAvailableError(Exception):
    def __init__(self):
        super(NoServersAvailableError, self).__init__("The JIT Scheduler found no available servers for this request.")

