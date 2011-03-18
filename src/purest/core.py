import httplib, uuid
import simplejson as json

class Collectd(object):
    @classmethod
    def post(cls, environ, start_response):
        body = environ['wsgi.input'].readlines()
        for ds in json.loads(''.join(body)):
            uid = str(uuid.uuid4())
            uri = "/collectd/%s" % uid
            conn = httplib.HTTPConnection("127.0.0.1", 5984)
            conn.request("PUT", uri, json.dumps(ds))
            res = conn.getresponse()

        response_headers = [('Content-type', 'text/plain')]
        status = '200 OK'

        start_response(status, response_headers)
        yield ''


class URIHandler(object):
    @classmethod
    def parse(cls, uri, method):
        if uri == '/collectd/data' and method == "POST":
            return Collectd.post
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
