""" core.py - Core objects of purest."""
from UserDict import DictMixin
from purest.app import collectd, metrics
from purest.uri import Map
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


class URIHandler(object):
    """Manage all uri/method routes."""
    def __init__(self):
        self._map = Map()

        # Just for convenience, needs to be moved into the app modules
        self._map.add(r'^/collectd/data', {'POST': collectd.Collectd.post})
        self._map.add(r'^/metrics/(?P<host>[\w]+)/(?P<plugin>[\w]+)/(?P<plugin_instance>[\w]+)/(?P<type>[\w]+)/(?P<type_instance>[\w]+)/$', 
                {'GET': metrics.Collection.all})

    def parse(self, request):
        """Take a uri and method and parse the the Map object for the right handler.

        :param: uri: string
        :param: method: string
        """

        #try:
        match = self._map.resolve(request['path'], request['method'])
        #except TypeError:
        #return URIHandler.fourofour

        return match

    def map(self, uri, method, handler):
        """Map a request using its uri and http method to the right handler."""
        self._map.add(uri, method, handler)

    @classmethod
    def fourofour(cls, start_response):
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
        handler, kwargs =  parser.parse(self.request)

        if handler:
            return handler(self.request, kwargs, self.start_response)
        else:
            return URIHandler.fourofour(self.start_response)

    def __call__(self):
        pass
