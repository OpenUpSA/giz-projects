from django.http import HttpResponsePermanentRedirect

class RedirectsMiddleware(object):
    """Always redirect www.host to host"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response is None:
            return self.get_response(request)
        else:
            return response
    
    def process_request(self, request):
        host = request.get_host()
        if host.startswith("www."):
            return HttpResponsePermanentRedirect("https://%s/" % host[4:])

