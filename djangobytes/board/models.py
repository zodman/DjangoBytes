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

# System imports
import os

# Django imports
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# DjangoBytes imports
from djangobytes import settings

class File(models.Model):
    file = models.FileField(_('File'), upload_to='filehosting')
    filename = models.CharField(_('Filename'), max_length=144)
    user = models.ForeignKey(User, verbose_name=_('User'))

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def __unicode__(self):
        return self.filename

class UserClass(models.Model):
    classname = models.CharField(_('Classname'), max_length=20)
    stars = models.IntegerField(_('Stars'))

    class Meta:
        verbose_name = _('User Class')
        verbose_name_plural = _('User Classes')

    def __unicode__(self):
        return self.classname

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=_('User'))
    passkey = models.CharField(_('Passkey'), max_length=32, blank=True, null=True)
    avatar = models.ForeignKey(File, verbose_name=_('Avatar'), blank=True, null=True)
    userclass = models.ForeignKey(UserClass, verbose_name=_('Userclass'), blank=True, null=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __unicode__(self):
        return self.user

class Invite(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    is_used = models.BooleanField(verbose_name=_('Used'))
    email = models.EmailField(max_length=100, verbose_name=_('E-Mail'))

    class Meta:
        verbose_name = _('Invite')
        verbose_name_plural = _('Invites')

    def __unicode__(self):
        return "{0} - {1}".format(user, is_active)

