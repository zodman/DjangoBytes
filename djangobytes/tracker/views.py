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
from django.conf import settings
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

# DjangoBytes imports
from djangobytes.src.inc.bencoding import encode, decode
from djangobytes.src.inc.utilities import manual_GET
from djangobytes.tracker.models import Torrent, Peer

def announce(request):
    # Parse a query string given as a string argument.
    qs = manual_GET(request)
    
    response_dict = {}
    
    # Check if there is an info_hash
    if qs.get('info_hash') is None:
        response_dict['failure reason'] = 'no request'
        return HttpResponse(encode(response_dict))

    # Create dict to collect the response parts.

    # encode info_hash
    info_hash = qs['info_hash'].encode('hex')
    
    # Check if there is a Torrent with this info_hash.
    try:
        torrent = Torrent.objects.get(info_hash=info_hash)
    except Torrent.DoesNotExist:
        # Torrent does not exist, so return failure reason.
        response_dict['failure reason'] = 'torrent not found'
        response_dict['interval'] = settings.ANNOUNCE_INTERVAL_NOTFOUND
        # Return bencoded response.
        return HttpResponse(encode(response_dict))

    # Check Request
    try:
        port = request.GET['port']
        event = request.GET.get('event')
        ip = request.META['REMOTE_ADDR']
    except MultiValueDictKeyError:
        # The request is invalid, so return failure reason.
        response_dict['failure reason'] = 'invalid request'
        response_dict['interval'] = settings.ANNOUNCE_INTERVAL_INVALIDREQUEST
        # Return bencoded response.
        return HttpResponse(encode(response_dict))

    # Process eventstate
    if 'started' in event:
        peer, created = Peer.objects.get_or_create(peer_id=peer_id, port=port, ip=ip, torrent=torrent)
        if created:
            peer.save()
    elif 'stopped' in event:
        try:
            peer = Peer.objects.get(peer_id=peer_id, ip=ip, torrent=torrent)
            peer.delete()
        except Peer.DoesNotExist:
            pass
    elif 'completed' in event:
        pass

    # Implement numwant - specifies how many peers the actual peer wants in his peerlist
    numwant = request.GET.get('numwant', settings.NUM_WANT)
    try:
        numwant = int(numwant)
    except TypeError:
        numwant = settings.NUM_WANT

    # Add existing peers, and interval to response_dict
    exist_peers = {}
    peers = Peer.objects.filter(torrent=torrent)
    peers[:numwant]
    for peer in peers:
        exist_peers.append({'id': peer.peer_id, 'ip': peer.ip, 'port': peer.port})
    response_dict['peers'] = exist_peers
    response_dict['interval'] = settings.ANNOUNCE_INTERVAL

    # Return bencoded response.
    return HttpResponse(encode(response_dict), mimetype='text/plain')
