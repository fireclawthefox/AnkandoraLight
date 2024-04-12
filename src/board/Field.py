#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class Field:
    def __init__(self, name, cost, special=""):
        self.connections = []

        self.name = name

        self.cost = cost

        self.special = special

        self.nodepath = None
