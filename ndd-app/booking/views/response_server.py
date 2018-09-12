from django.shortcuts import render_to_response
from django.template import RequestContext


def error_404(request, *args, **argv):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def error_500(request, *args, **argv):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response