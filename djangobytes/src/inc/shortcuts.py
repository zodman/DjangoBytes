# System imports
import os
import mimetypes

# Django imports
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.encoding import smart_str

"""Keep your usefull tools here
"""

def csrf_render(request, tpl, tplvars={}, forms_errors=None):
    """Shortcut for renewing csrf cookie and passing request context
    
    Keyword arguments:
    tpl -- the template we want to use
    args -- the template variables

    """
    tplvars.update(csrf(request))
    # pass config vars
    tplvars['forms_errors'] = forms_errors
    return render_to_response(tpl, tplvars,
                               context_instance=RequestContext(request))
