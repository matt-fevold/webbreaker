#!/usr/bin/env python
# -*-coding:utf-8-*-

from pybreaker import CircuitBreaker, CircuitBreakerListener
from webbreaker.common.webbreakerlogger import Logger


class CircuitBreakerHelper(CircuitBreaker):
    fail_max = 2
    reset_timeout = 30


class APIListener(CircuitBreakerListener):
    "Listener used by circuit breakers that execute api operations."

    def before_call(self, callback, func, *args, **kwargs):
        "Called before the circuit breaker `cb` calls `func`."
        pass

    def state_change(self, callback, old_state, new_state):
        "Called when the circuit breaker `cb` state changes."
        pass

    def failure(self, callback, execution):
        "Called when a function invocation raises a system error."
        pass

    def success(self, callback):
        "Called when a function invocation succeeds."
        pass


class LogListener(CircuitBreakerListener):
    "Listener used to log circuit breaker events."

    def state_change(self, callback, old_state, new_state):
        msg = "State Change: callback: {0}, New State: {1}".format(callback.name, new_state)
        Logger.app.error("{}".format(msg))

