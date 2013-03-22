
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.shortcuts import redirect

from django.template import RequestContext

@login_required(login_url='/admin/')
def match_view(request):
    return render_to_response("dna/match.html", locals(), context_instance=RequestContext(request))

