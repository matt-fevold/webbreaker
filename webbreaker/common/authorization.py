#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click import prompt


def auth_prompt(service_name):
    username = prompt('{} user'.format(service_name))
    password = prompt('{} password'.format(service_name), hide_input=True)
    return username, password
