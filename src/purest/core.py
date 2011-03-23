""" core.py - Core objects of purest."""
from UserDict import DictMixin
from purest.app import collectd
import httplib, uuid
import simplejson as json


class Request(DictMixin):
    """A dictionary representation of a HTTP request."""
    def __init__(self, environ):
        self._req = {}
        for key, value in environ.iteritems():
            if key in "REQUEST_METHOD":
                self._req['method'] = value
            elif key in "PATH_INFO":
                self._req['path'] = value
            else:
                self._req[key.lower()] = value

    def __getitem__(self, key):
        """Return the value of the given key. 

        Raises `KeyError` if not existing.'''
        :param: key: string
        """
        try:
            value = self._req[key]
        except:
            raise KeyError

        return value

    def __setitem__(self, key, value):
        """Set a variable.

        :param: key: string
        :param: value: string
        """
        self._req[key] = value

    def __delitem__(self, key):
        """Delete a variable.

        :param: key: string
        """
        try:
            del self._req[key]
        except:
            raise KeyError

    def __iteritems__(self):
        """Return all key value pairs as an iterator."""
        return self._req.iteritems()

    def keys(self):
        '''Return all variable names.'''
        return self._req.keys()

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

    def parse(self, request):
        """Take a uri and method and parse the the Map object for the right handler.i

        :param: uri: string
        :param: method: string
        """
        #try:
        self._map.routes[request['path']][request['method']]
        #except TypeError:
        #return URIHandler.fourofour

        return self._map.routes[request['path']][request['method']]

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
        self.request = Request(environ)
        self.start_response = start_response

    def __iter__(self):
        # Create a new parser and parse the request.
        parser = URIHandler()
        handler =  parser.parse(self.request)
        return handler(self.request, self.start_response)

    def __call__(self):
        pass
