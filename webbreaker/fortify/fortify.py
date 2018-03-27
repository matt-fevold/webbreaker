#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.fortify.fortify_config import FortifyConfig


class Fortify:
    def __init__(self):
        self.config = None

    def _set_config_(self):
        self.config = FortifyConfig()


