from django.shortcuts import redirect


class Redirect404Middleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return redirect('/404/')

        return response
