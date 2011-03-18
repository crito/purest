""" core.py - Core objects of purest."""
from purest.app import collectd

class URIHandler(object):
    """Manage all uri/method routes."""
    @classmethod
    def parse(cls, uri, method):
        """Take a uri and method and parse the the Map object for the right handler."""
        if uri == '/collectd/data' and method == "POST":
            return collectd.Collectd.post
        else:
            return URIHandler.fourofour

    def map_request(self, uri, method):
        """Map a request using its uri and http method to the right handler."""
        pass

    @classmethod
    def fourofour(cls, environ, start_response):
        response_headers = [('Content-type', 'text/plain')]
        status = '404 Not Found'

        start_response(status, response_headers)
        yield ''


class WSGI(object):
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        handler =  URIHandler.parse(self.environ['PATH_INFO'], self.environ['REQUEST_METHOD'])
        return handler(self.environ, self.start_response)

    def __call__(self):
        pass
