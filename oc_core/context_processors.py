import socket


def server_name(request):

    try:
        hostname = socket.gethostname()
    except:
        hostname = 'localhost'

    return {'server_name': hostname}


import wagtail
if wagtail.VERSION[0] >= 2:
    from wagtail.core.models import Site
else:
    from wagtail.wagtailcore.models import Site

def site(request):
    return {
        'site': Site.find_for_request(request)
    }