import httplib, uuid
import simplejson as json
import couchdb

def send_message(host, port, uri, method, body=""):
    conn = httplib.HTTPConnection(host, port)
    conn.request(method, uri, body)
    return conn.getresponse()

class Collectd(object):
    @classmethod
    def post(cls, request, kwargs, start_response):
        """Post a new (time,[values,]) tuple to the backend."""
        body = request['wsgi.input'].readlines()
        #couchserver = couchdb.client.Server()
        for data_set in json.loads(''.join(body)):
            uid = str(uuid.uuid4())
            db = "%s-%s-%s-%s-%s" % ('_'.join(data_set['host'].split('.')), 
                    data_set['plugin'], data_set['plugin_instance'], 
                    data_set['type'], data_set['type_instance'])

            # Using the couchdb api
            #try:
            #    db = couchserver[db]
            #except couchdb.http.ResourceNotFound:
            #    couchserver.create(db)
            #    db = couchserver[db]

            doc = {
                "time": data_set['time'],
                "values": data_set['values']
                }
            #doc_id, doc_rev = db.save(doc)

            res = send_message("127.0.0.1", "5984", "/%s/%s" % (db, uid), "PUT", json.dumps(doc))

            # If the db doesn't exist. Test for a 400 return code.
            if res.status == 404:
                res = send_message("127.0.0.1", "5984", "/%s" % (db), "PUT")
                view = {
                        "_id": "_design/basic",
                        "views": {
                            "all": {
                                "map": "function(doc) {\nemit(doc.time, doc.values);\n}"
                            }
                        }
                    }
                res = send_message("127.0.0.1", "5984", "/%s/_design/basic/" % db, "PUT", json.dumps(view))
                res = send_message("127.0.0.1", "5984", "/%s/%s" % (db, uid), "PUT", json.dumps(doc))

        response_headers = [('Content-type', 'text/plain')]
        status = '200 OK'

        start_response(status, response_headers)
        yield ''

