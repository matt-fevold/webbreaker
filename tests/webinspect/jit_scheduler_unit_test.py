import mock
import pytest

from webbreaker.webinspect.jit_scheduler import WebInspectJitScheduler, NoServersAvailableError
try:  # python 3
    from queue import Queue, Empty
except ImportError:  # python 2
    from Queue import Queue as queue


# need to mock is_available so no api calls are made.
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectConfig')
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectJitScheduler._is_endpoint_available')
def test_jit_scheduler_success(is_endpoint_available_mock, config_mock):

    endpoints = [['some_server1.com:8083', '1'],
                 ['some_server2.com:8083', '2'],
                 ]
    config_mock.return_value.endpoints = endpoints

    jit = WebInspectJitScheduler(server_size_needed='large',
                                 username='user', password='pass')

    # Sadly this is a bit complex - is_available is supposed to add available endpoints to a queue
    is_endpoint_available_mock.side_effect = jit._results_queue.put(endpoints[1], False)

    result_endpoint = jit.get_endpoint()

    assert result_endpoint == 'some_server2.com:8083'


# need to mock is_available so no api calls are made.
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectConfig')
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectJitScheduler._is_endpoint_available')
def test_jit_scheduler_small_server_success(is_endpoint_available_mock, config_mock):

    endpoints = [['some_server1.com:8083', '1'],
                 ['some_server2.com:8083', '2'],
                 ]
    config_mock.return_value.endpoints = endpoints

    jit = WebInspectJitScheduler(server_size_needed='small',
                                 username='user', password='pass')

    # Sadly this is a bit complex - is_available is supposed to add available endpoints to a queue
    is_endpoint_available_mock.side_effect = jit._results_queue.put(endpoints[0], False)

    result_endpoint = jit.get_endpoint()

    assert result_endpoint == 'some_server1.com:8083'


# need to mock is_available so no api calls are made.
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectConfig')
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectJitScheduler._is_endpoint_available')
def test_jit_scheduler_medium_server_success(is_endpoint_available_mock, config_mock):

    endpoints = [['some_server1.com:8083', '1'],
                 ['some_server2.com:8083', '2'],
                 ]
    config_mock.return_value.endpoints = endpoints

    jit = WebInspectJitScheduler(server_size_needed='medium',
                                 username='user', password='pass')

    # Sadly this is a bit complex - is_available is supposed to add available endpoints to a queue
    is_endpoint_available_mock.side_effect = jit._results_queue.put(endpoints[0], False)

    result_endpoint = jit.get_endpoint()

    assert result_endpoint == 'some_server1.com:8083'

# need to mock is_available so no api calls are made.
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectConfig')
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectJitScheduler._is_endpoint_available')
def test_jit_scheduler_large_server_multiple_same_sized_endpoints_choose_first_success(is_endpoint_available_mock,
                                                                                       config_mock):
    # test to make sure whichever adds to the queue first is chosen (first endpoint wins)
    endpoints = [['some_server1.com:8083', '2'],
                 ['some_server2.com:8083', '2'],
                 ]
    config_mock.return_value.endpoints = endpoints

    jit = WebInspectJitScheduler(server_size_needed='large',
                                 username='user', password='pass')

    # pick an endpoint
    endpoint = endpoints[0]

    # Sadly this is a bit complex - is_available is supposed to add available endpoints to a queue
    is_endpoint_available_mock.side_effect = jit._results_queue.put(endpoint, False)

    result_endpoint = jit.get_endpoint()

    assert result_endpoint == endpoint[0]


# need to mock is_available so no api calls are made.
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectConfig')
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectJitScheduler._is_endpoint_available')
def test_jit_scheduler_large_server_multiple_same_sized_endpoints_choose_second_success(is_endpoint_available_mock,
                                                                                        config_mock):
    # test to make sure whichever adds to the queue first is chosen (second endpoint wins)
    endpoints = [['some_server1.com:8083', '2'],
                 ['some_server2.com:8083', '2'],
                 ]
    config_mock.return_value.endpoints = endpoints

    jit = WebInspectJitScheduler(server_size_needed='large',
                                 username='user', password='pass')

    # pick an endpoint
    endpoint = endpoints[1]

    # Sadly this is a bit complex - is_available is supposed to add available endpoints to a queue
    is_endpoint_available_mock.side_effect = jit._results_queue.put(endpoint, False)

    result_endpoint = jit.get_endpoint()

    assert result_endpoint == endpoint[0]



# need to mock is_available so no api calls are made.
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectConfig')
@mock.patch('webbreaker.webinspect.jit_scheduler.WebInspectJitScheduler._is_endpoint_available')
def test_jit_scheduler_no_available_servers_raise_no_available_servers_errror(is_endpoint_available_mock,
                                                                              config_mock):
    endpoints = [['some_server1.com:8083', '1'],
                 ['some_server2.com:8083', '2'],
                 ]
    config_mock.return_value.endpoints = endpoints

    jit = WebInspectJitScheduler(server_size_needed='large',
                                 username='user', password='pass', timeout=.1)

    # thought this would raise either a TimeoutError or NoServersAvailable
    # but this was kinda weird.
    with pytest.raises(NoServersAvailableError):
        jit.get_endpoint()
