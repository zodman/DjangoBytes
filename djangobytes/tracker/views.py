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
import urllib
from struct import pack
from socket import inet_aton

# Django imports
from django.conf import settings
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

# DjangoBytes imports
from djangobytes.src.inc.benc import bdecode, bencode
from djangobytes.src.inc.shortcuts import manual_GET
from djangobytes.tracker.models import Torrent, Peer

def failureResponse(failure_reason=None, failure_code=None, interval=None):
    response = {}
    if not failure_reason:
        failure_reason = 'Invalid Request'
    if not interval:
        interval = settings.ANNOUNCE_INTERVAL_INVALIDREQUEST
    response['failure reason'] = failure_reason
    if failure_code:
        response['failure code'] = failure_code
    response['interval'] = interval
    return HttpResponse(bencode(response))

def announce(request):
    # Parse a query string given as a string argument.
    qs = manual_GET(request)
    
    # Create dict to collect the response parts.
    response_dict = {}
    
    # Check if there is an info_hash
    if qs.get('info_hash') is None:
        failureResponse(failure_code=101)

    # get info_hash
    info_hash = qs.get('info_hash')

    # encode info_hash
    try:
        info_hash = urllib.unquote_plus(info_hash)
        info_hash = info_hash.encode('hex')
    except: # TODO: search correct exception
        failureResponse(failure_reason='Invalid info_hash')       

    # Check if there is a Torrent with this info_hash.
    try:
        torrent = Torrent.objects.get(info_hash=info_hash)
    except Torrent.DoesNotExist:
        # Torrent does not exist, so return failure reason.
        failureResponse(failure_reason='Torrent not found', failure_code=200, interval=settings.ANNOUNCE_INTERVAL_NOTFOUND)

    # Check Request
    try:
        port = request.GET['port']
        event = request.GET.get('event', '')
        peer_id = request.GET.get('peer_id')
        ip = request.META.get('REMOTE_ADDR')
    except MultiValueDictKeyError:
        # The request is invalid, so return failure reason.
        failureResponse()

    announce_method_options = ['compact', 'no_peer_id']
    announce_method_results = {}
    for key in announce_method_options:
        if not request.GET.get(key):
            announce_method_results[key] = False
        else:
            announce_method_results[key] = request.GET.get(key)
            try:
                announce_method_results[key] = int(announce_method_results[key])
            except ValueError:
                # if string is not convertable to integer, set the given method to false
                announce_method_results[key] = False
            if announce_method_results[key] == 1:
                announce_method_results[key] = True
            else:
                # if given method is a integer and if it's not 1, the given method is invalid!
                # to prevent of sending a failure response, set the given method to false
                # this means, that the tracker sends a standard response to the client
                announce_method_results[key] = False

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
    elif 'completed' in event or '' in event:
        pass

    # Implement numwant - specifies how many peers the actual peer wants in his peerlist
    numwant = request.GET.get('numwant', settings.NUM_WANT)
    try:
        numwant = int(numwant)
    except TypeError:
        numwant = settings.NUM_WANT

    # Add existing peers, and interval to response_dict
    exist_peers = []
    peers = Peer.objects.filter(torrent=torrent)
    peers[:numwant]

    if announce_method_results['compact'] == True:
        print('DEBUG:   compact response')
        exist_peers = ""
        for peer in peers:
            exist_peers += pack('>4sH', inet_aton(peer.ip), peer.port)

    elif announce_method_results['no_peer_id'] == True:
        print('DEBUG:   no_peer_id response')
        exist_peers = []
        for peer in peers:
            exist_peers.append({'ip': peer.ip, 'port': peer.port})
    else:
        print('DEBUG:   standard response')
        exist_peers = []
        for peer in peers:
            exist_peers.append({'peer id': peer.peer_id, 'ip': peer.ip, 'port': peer.port})
    
    response_dict['peers'] = exist_peers
    response_dict['interval'] = settings.ANNOUNCE_INTERVAL

    # Return bencoded response.
    return HttpResponse(bencode(response_dict))
