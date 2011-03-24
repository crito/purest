import httplib, uuid
import simplejson as json
import couchdb
from collections import defaultdict

def send_message(host, port, uri, method, body=""):
    conn = httplib.HTTPConnection(host, port)
    conn.request(method, uri, body)
    return conn.getresponse()

class Collection(object):
    class recursivedict(defaultdict):
        def __init__(self):
            self.default_factory = type(self)

    @classmethod
    def all(cls, request, kwargs, start_response):
        """Return all collections. Filter by kwargs."""
        collections = cls.recursivedict()
        # Get all db's and fill the collections dict:
        dbs = send_message("127.0.0.1", "5984", '/_all_dbs', 'GET')
        # FIXME: Check return message
        all_dbs = json.loads(dbs.read())
        for i in all_dbs:
            parts = i.split('-')
            hostname = '.'.join(parts[0].split('_'))
            for j in range(1, len(parts)):
                if parts[j] == '':
                    parts[j] = '-'
            collections[hostname][parts[1]][parts[2]][parts[3]] = parts[4]

        for kk in sorted(collections.keys()):
            print "-",kk
            for jj in sorted(collections[kk].keys()):
                print "  -",jj
                for ii in sorted(collections[kk][jj].keys()):
                    print "    -",ii
                    for hh in sorted(collections[kk][jj][ii].keys()):
                        print "      -",hh,collections[kk][jj][ii][hh]

        response_headers = [('Content-type', 'text/plain')]
        status = '200 OK'

        start_response(status, response_headers)
        yield ''

