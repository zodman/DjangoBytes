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
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
	url(r'^tracker/', include('djangobytes.tracker.urls', namespace='tracker', app_name='tracker')),
        url(r'^board/', include('djangobytes.board.urls', namespace='board', app_name='board')),
        url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    urlpatterns  += patterns("",
         (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT, "show_indexes":True, }),
        ) + staticfiles_urlpatterns()

