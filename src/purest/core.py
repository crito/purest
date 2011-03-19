""" core.py - Core objects of purest."""
from purest.app import collectd
import httplib, uuid
import simplejson as json


class Request(object):
    """A dictionary representation of a HTTP request."""
    pass

class Map(object):
    """Maps between uri/methods and handlers."""
    def __init__(self):
        self._routes = {}

    def add(self, uri, method, handler):
        """Add a new route to the map.

        :param: uri: string
        :param: method: string
        :param: handler: callable
        """
        self._routes[uri] = { method: handler }

    @property
    def routes(self):
        """Return all stored map routes."""
        return self._routes

class URIHandler(object):
    """Manage all uri/method routes."""
    def __init__(self):
        self._map = Map()
        self._map.add('/collectd/data', 'POST', collectd.Collectd.post)

    def parse(self, uri, method):
        """Take a uri and method and parse the the Map object for the right handler.i

        :param: uri: string
        :param: method: string
        """
        #try:
        self._map.routes[uri][method]
        #except TypeError:
        #return URIHandler.fourofour

        return self._map.routes[uri][method]

    def map(self, uri, method, handler):
        """Map a request using its uri and http method to the right handler."""
        self._map.add(uri, method, handler)

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
        # Create a new parser and parse the request.
        parser = URIHandler()
        handler =  parser.parse(self.environ['PATH_INFO'], self.environ['REQUEST_METHOD'])
        return handler(self.environ, self.start_response)

    def __call__(self):
        pass
