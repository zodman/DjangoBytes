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
import os.path
import sys

# Install directory
INSTALL_DIR = os.path.dirname( os.path.abspath(__file__) )

# SSL stuff
# SESSION_COOKIE_SECURE = True 
SESSION_COOKIE_SECURE = False #<-- during develop processes....

# Django configuration
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
      ('Dominic Miglar', 'war10ck@iirc.cc'),
      ('Angelo Gründler', 'me@kanadezwo.ch')
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(INSTALL_DIR, 'db.sqlite3'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-MX'

SITE_ID = 1

# Available languages
_ = lambda s: s

LANGUAGES = (
      ('de', _('German')),
      ('en', _('English')),
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

ROOT_URLCONF = 'urls'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(INSTALL_DIR, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(INSTALL_DIR, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4qe66$(@x=^*ak*_d_(+n6r+l7(kv6$owvouz(#)l#%hmz$h)%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'djangobytes.board.middleware.RequireLoginMiddleware',
    'djangobytes.board.middleware.RequireStaffMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(INSTALL_DIR, 'templates'),
    # Put strings here, like '/home/html/django_templates' or 'C:/www/django/templates'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'tracker',
    'board',
)

#TEMPLATE_CONTEXT_PROCESSORS = (
    #"django.contrib.auth.context_processors.auth",
    #"django.core.context_processors.request",
    #"django.core.context_processors.i18n",
    #"django.core.context_processors.static",
    #'django.contrib.messages.context_processors.messages',
#)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Board Settings
LOGIN_REQUIRED_URLS = (
    r'/(.*)$',
)

LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/board/login(.*)$', 
    r'/board/logout(.*)$',
    r'/tracker/announce(.*)$',
    r'/board/config/setup/(.*)$',
    r'/static/djangobytes/css/login.css(.*)$',
    r'/static/djangobytes/css/normalize.css(.*)$',
    r'/static/serverkiller/favicon.ico(.*)$',
)

LOGIN_URL = '/board/login/'

LOGIN_REDIRECT_URL = '/'

STAFF_REQUIRED_URLS = {
    r'/board/config(.*)$',
}

STAFF_REQUIRED_URLS_EXCEPTIONS = (
    r'/board/config/setup(.*)$',
)

INS_PERMISSIONS_URL = '/'

PASSKEY_LENGTH = 32

# REQUIRE_ANNOUNCE_METHON can be 'standard', 'no_peer_id, or 'compact' (not implemented)
REQUIRE_ANNOUNCE_METHOD = 'standard'

# standard num_want, if client doesn't specify it itself
NUM_WANT = 50

# announce interval, in seconds
ANNOUNCE_INTERVAL = 120
ANNOUNCE_INTERVAL_NOTFOUND = 420
ANNOUNCE_INTERVAL_INVALIDREQUEST = 600

