from django.http import Http404
from django.shortcuts import redirect


class Redirect404Middleware(object):
    def process_response(self, request, response):
        if response == Http404:
            return redirect('/404/')

        return response