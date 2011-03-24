import httplib, uuid
import simplejson as json
import couchdb
from collections import defaultdict

def send_message(host, port, uri, method, body=""):
    conn = httplib.HTTPConnection(host, port)
    conn.request(method, uri, body)
    return conn.getresponse()


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class Collection(object):
    @classmethod
    def all(cls, request, kwargs, start_response):
        """Return all collections. Filter by kwargs."""
        #
        collection = AutoVivification()
        # Get all db's and fill the collections dict:
        dbs = send_message("127.0.0.1", "5984", '/_all_dbs', 'GET')
        # FIXME: Check return message
        all_dbs = json.loads(dbs.read())
        for i in all_dbs:
            parts = i.split('-')
            parts[0] = '.'.join(parts[0].split('_'))
            for j in range(1, len(parts)):
                if parts[j] == '':
                    parts[j] = '-'

            collection[parts[0]][parts[1]][parts[2]][parts[3]][parts[4]] = []

        response_headers = [('Content-type', 'text/plain')]
        status = '200 OK'

        start_response(status, response_headers)
        yield json.dumps(collection)

