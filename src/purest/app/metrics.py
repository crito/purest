import httplib
import uuid
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
    def __init__(self):
        """Fill a nested dictionary with all available databases."""
        self.collection = AutoVivification()
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

            self.collection[parts[0]][parts[1]][parts[2]][parts[3]][parts[4]] = []

    def reduce(self):
        return self.collection

    @classmethod
    def all(cls, request, kwargs, start_response):
        """Return all collections. Filter by kwargs."""
        collection = cls()

        response_headers = [('Content-type', 'text/plain')]
        status = '200 OK'

        start_response(status, response_headers)
        yield json.dumps(collection.reduce())

    @classmethod
    def filter(cls, request, kwargs, start_response):
        """Return a list of json objects, each object being one table of x/y values.

        The uri gets dissected into tokens. Each token is parsed using the following grammar:

        1) test if token is '-':  --> select all members of the token
        2) test if a ';' splits the token:  --> a list of unordered members of the token
        3) test if any object is split by a '-':  --> a list of a range of members of the token
        """
        # tokens[0]  --> hostnames
        # tokens[1]  --> plugins
        # tokens[2]  --> plugin_instances
        # tokens[3]  --> types
        # tokens[4]  --> type_instances
        tokens = []
        tokens.append(kwargs['host'] if kwargs['host'] != 'x' else '')
        tokens.append(kwargs['plugin'] if kwargs['plugin'] != 'x' else '')
        tokens.append(kwargs['plugin_instance'] if kwargs['plugin_instance'] != 'x' else '')
        tokens.append(kwargs['type'] if kwargs['type'] != 'x' else '')
        tokens.append(kwargs['type_instance'] if kwargs['type_instance'] != 'x' else '')

        print tokens
        # clean hostname
        tokens[0] = '_'.join(tokens[0].split('.'))
        db = '-'.join(tokens)
        data = send_message('127.0.0.1', '5984', '/%s/_design/basic/_view/all/' % db, 'GET')
        data = json.loads(data.read())

        response_headers = [('Content-type', 'text/plain')]
        status = '200 OK'

        start_response(status, response_headers)
        yield json.dumps(data)
        # Creates a nested dictionary containing the whole collection structure
        #dbs = cls()
