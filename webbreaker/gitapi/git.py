#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import ntpath
import logging
import requests
import urllib3
import requests.exceptions
import requests.packages.urllib3


class GitApi(object):
    def __init__(self, host, token, verify_ssl=True):
        if 'github.com' in host:
            self.host = 'https://api.github.com'
        else:
            self.host = host + '/api/v3'
        self.token = token
        self.verify_ssl = verify_ssl

        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    def get_user(self, login):
        """
        :param GitHub login of user
        :return: All public information for user
        """
        return self._request('GET', '/users/' + login)

    def get_contributors(self, owner, repo):
        """
        :param Owner of repo and repo name
        :return: All logins of contributors to this repo
        """
        return self._request('GET', "/repos/{}/{}/contributors".format(owner, repo))


    def _request(self, method, url):
        try:
            logger('Performing method {}'.format(method))
            logger('URL {}'.format(self.host + url))
            auth = "?access_token=" + self.token
            response = requests.request(method=method, url=self.host + url + auth, verify=self.verify_ssl)

            logger('Response status code: {}'.format(str(response.status_code)))

            try:
                response.raise_for_status()

                response_code = response.status_code
                success = True if response_code == 200 else False
                if response.text:
                    data = response.json()
                else:
                    data = ''

                return GitResponse(success=success, response_code=response_code, data=data)
            except ValueError as e:
                return GitResponse(success=False, message="JSON response could not be decoded {}.".format(e))
        except requests.exceptions.SSLError:
            return GitResponse(message='An SSL error occurred.', success=False)
        except requests.exceptions.ConnectionError:
            return GitResponse(message='A connection error occurred.', success=False)
        except requests.exceptions.Timeout:
            return GitResponse(message='The request timed out after ', success=False)
        except requests.exceptions.RequestException:
            return GitResponse(
                message='There was an error while handling the request. {}'.format(response.content), success=False)


class GitResponse(object):
    """Container for all Git API responses, even errors."""

    def __init__(self, success, message='OK', response_code=-1, data=None):
        self.message = message
        self.success = success
        self.response_code = response_code
        self.data = data

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return self.message

    def data_json(self, pretty=False):
        """Returns the data as a valid JSON string."""
        if pretty:
            return json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self.data)

def logger(name):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)

    return logger
