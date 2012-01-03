#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
DjangoBytes

Copyright (C) 2011 Dominic Miglar, war10ck@iirc.cc
Copyright (C) 2011 Angelo Gründler, me@kanadezwo.ch

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

# Base imports
import re

# Django imports
from django.conf import settings
from django.contrib.auth.decorators import login_required

# DjangoBytes imports
from djangobytes.board.views.decorators import staff_required

class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around 
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and 
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your 
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$', 
        r'/topsecret/logout(.*)$',
    )
    ------                 
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must 
    be a valid regex.     

    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly 
    define any exceptions (like login and logout URLs).
    """
    def __init__(self):
        self.required = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS])
        self.exceptions = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS])

    def process_view(self,request,view_func,view_args,view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated(): return None
        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path): return None
        # Requests matching a restricted URL pattern are returned 
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path): return login_required(view_func)(request,*view_args,**view_kwargs)
        # Explicitly return None for all non-matching requests
        return None

class RequireStaffMiddleware(object):
    """
    Middleware component that wraps the staff_required decorator around 
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and 
    define STAFF_REQUIRED_URLS and STAFF_REQUIRED_URLS_EXCEPTIONS in your 
    settings.py. For example:
    ------
    STAFF_REQUIRED_URLS = (
        r'/admin/(.*)$',
    )
    STAFF_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$', 
        r'/topsecret/logout(.*)$',
    )
    ------                 
    STAFF_REQUIRED_URLS is where you define URL patterns; each pattern must 
    be a valid regex.     

    STAFF_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly 
    define any exceptions (like login and logout URLs).
    """
    def __init__(self):
        self.required = tuple([re.compile(url) for url in settings.STAFF_REQUIRED_URLS])
        self.exceptions = tuple([re.compile(url) for url in settings.STAFF_REQUIRED_URLS_EXCEPTIONS])

    def process_view(self,request,view_func,view_args,view_kwargs):
        if request.user.is_staff: return None
        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path): return None
        # Requests matching a restricted URL pattern are returned 
        # wrapped with the staff_required decorator
        for url in self.required:
            if url.match(request.path): return staff_required(view_func)(request,*view_args,**view_kwargs)
        # Explicitly return None for all non-matching requests
        return None
