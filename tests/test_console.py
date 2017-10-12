#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from webbreaker.__main__ import cli


class TestConsole(TestCase):
    def test_basic(self):
        cli()
