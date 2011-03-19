import httplib, uuid
import simplejson as json

class Collectd(object):
    @classmethod
    def post(cls, environ, start_response):
        body = environ['wsgi.input'].readlines()
        for data_set in json.loads(''.join(body)):
            uid = str(uuid.uuid4())
            uri = "/collectd/%s" % uid
            conn = httplib.HTTPConnection("127.0.0.1", 5984)
            conn.request("PUT", uri, json.dumps(data_set))
            res = conn.getresponse()

        response_headers = [('Content-type', 'text/plain')]
        status = '200 OK'

        start_response(status, response_headers)
        yield ''
