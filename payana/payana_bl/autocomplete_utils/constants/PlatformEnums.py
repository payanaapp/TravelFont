#!/usr/bin/env python

"""Defines the different platforms - web, android and ios
"""
import enum


class PlatformEnums(str, enum.Enum):

    Android = "android"
    Web = "web"
    ios = "ios"
