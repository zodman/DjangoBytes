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
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# DjangoBytes imports
from djangobytes import settings
from djangobytes.board.models import UserProfile

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm password'), required=False, widget=forms.PasswordInput)
    is_staff = forms.BooleanField(label=_('Superuser'),
        help_text=_('Sets if the user is a staff.'), required=False)
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_superuser' 'last_login',
                   'date_joined', 'groups', 'user_permissions', 'password')

    def clean_password2(self):
        """Password confirmation checker
        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        """Sets the password for the user on save
        
        Keyword arguments:
        commit -- True if the values should be saved into the db
        """
        user = super(UserForm, self).save(commit=False)
        # dont save password if the password field is empty
        if self.cleaned_data["password1"] != '':
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user', 'avatar', 'passkey', 'userclass')
