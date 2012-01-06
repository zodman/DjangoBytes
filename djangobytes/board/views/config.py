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

# Django imports
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, render, render_to_response, RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

#DjangoBytes imports
from djangobytes.board.forms import *
from djangobytes.src.inc.shortcuts import *

def config_settings(request):
    return render_to_response('board/config/settings.html', context_instance=RequestContext(request))

def config_settings_new_user(request):
    """
    The admin view for creating a new user
    """
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.passkey = passkey_generator()
            profile.save()
            return HttpResponseRedirect(reverse('board:config_settings'))
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return csrf_render(request, 'board/config/settings_new_user.html', ctx, True)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()   
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return csrf_render(request, 'board/config/settings_new_user.html', ctx)

