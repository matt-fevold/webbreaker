#!/usr/bin/env python
# -*-coding:utf-8-*-

from pybreaker import CircuitBreaker, CircuitBreakerListener
from webbreaker.common.webbreakerlogger import Logger


class CircuitBreakerHelper(CircuitBreaker):
    FAIL_MAX = fail_max = 2
    RESET_TIMEOUT = reset_timeout = 30


class APIListener(CircuitBreakerListener):
    "Listener used by circuit breakers that execute api operations."

    def before_call(self, cb, func, *args, **kwargs):
        "Called before the circuit breaker `cb` calls `func`."
        pass

    def state_change(self, cb, old_state, new_state):
        "Called when the circuit breaker `cb` state changes."
        pass

    def failure(self, cb, exc):
        "Called when a function invocation raises a system error."
        pass

    def success(self, cb):
        "Called when a function invocation succeeds."
        pass


class LogListener(CircuitBreakerListener):
    "Listener used to log circuit breaker events."

    def state_change(self, cb, old_state, new_state):
        msg = "State Change: callback: {0}, New State: {1}".format(cb.name, new_state)
        Logger.app.info("{}".format(msg))
