.. image::
   https://github.com/kanadezwo/DjangoBytes/raw/master/res/djangobytes-logo.png

:Version: 0.1.0
:Keywords: djangobytes, django, bittorrent, tracker, alt, python

DjangoBytes is a new and improved BitTorrent tracker based on Django.

License (MIT)
=============

Copyright (C) 2011 Dominic Miglar and Angelo Gründler

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

Versioning
==========

Releases will be numbered with the follow format::

    <major>.<minor>.<patch>

And constructed with the following guidelines:

* Breaking backwards compatibility bumps the major
* New additions without breaking backwards compatibility bumps the minor
* Bug fixes and misc changes bump the patch

We use even stable odd unstable versioning, e.g. 0.1 would be unstable whereas 
0.2 would be stable.

Bug tracker
===========

If you have any suggestions, bug reports or annoyances please report them
to our issue tracker at http://github.com/kanadezwo/DjangoBytes/issues.

Installation (development)
==========================

Create a virtualenv::

    virtualenv --python=python2.7 dev
    source dev/bin/activate

Install all dependencies::

    pip install bjoern django pil pysqlite

Run DjangoBytes
===============

It's simple and easy::

    source dev/bin/activate
    python djangobytes/manage.py syncdb
    python djangobytes/run_bjoern.py 127.0.0.1 22446

DjangoBytes is now running on http://127.0.0.1:22446/.

Nginx (SSL)
===========

It's also simple and easy::

    server {
            listen 80;
            server_name yourdomain.tdl;
            rewrite     ^(.*)   https://$server_name$1 permanent;
    }

    server {
            listen 443;
            ssl                  on;
            ssl_certificate      /path/to/your/cert.crt;
            ssl_certificate_key  /path/to/your/cert.key;
            server_name yourdomain.tdl;
            location / {
                    proxy_pass http://127.0.0.1:22446;
                    proxy_redirect off;

                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Protocol https;

                    client_max_body_size 10m;
                    client_body_buffer_size 128k;

                    proxy_connect_timeout 90;
                    proxy_send_timeout 90;
                    proxy_read_timeout 90;

                    proxy_buffer_size 4k;
                    proxy_buffers 4 32k;
                    proxy_busy_buffers_size 64k;
                    proxy_temp_file_write_size 64k;
            }
    }


Initial setup
=============

You can start with the initial setup at https://ip:port/board/config/setup.

Production Deployments
======================

The following BitTorrent-Trackers are powered by DjangoBytes:

.. image::
   https://github.com/kanadezwo/DjangoBytes/raw/master/res/serverkiller-logo.png

Contact
=======

IRC
---

We reside on irc.freenode.net in channel ``#djangobytes``.

Thanks
======

Thanks to Bernhard Posselt, who has helped us to fix various problems.

