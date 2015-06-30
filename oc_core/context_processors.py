import socket


def server_name(request):

    try:
        hostname = socket.gethostname()
    except:
        hostname = 'localhost'

    return {'server_name': hostname}



from wagtail.wagtailcore.models import Site

def site(request):
    return {
        'site': Site.find_for_request(request)
    }