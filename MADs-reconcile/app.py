from flask import Flask, request, jsonify, json
from mads_parse import MADsParser

app = Flask(__name__)

refine_to_lc = list([
    {
        "id": "Names",
        "name": "Library of Congress Name Authority File",
        "index": "/authorities/names"
    },
    {
        "id": "Subjects",
        "name": "Library of Congress Subject Headings",
        "index": "authorities/subjects"

    }
])

query_types = [{'id': item['id'], 'name': item['name']} for item in refine_to_lc]

metadata = {
    "name": "MADs Reconciliation Service",
    "identifierSpace" : "http://localhost/identifier",
    "schemaSpace" : "http://localhost/schema",
    "defaultTypes": query_types,
    "view": {
        "url": "{{id}}"
    },
}

def jsonpify(obj):
    try:
        callback = request.args['callback']
        response = app.make_response("%s(%s)" % (callback, json.dumps(obj)))
        response.mimetype = "text/javascript"
        return response
    except KeyError:
        return jsonify(obj)

# maybe move this over to mads_parse
def search(search_in, query_type='', limit=3):
    # this will search the dictionary
    # import parse as a module, have a function from there return a dict
    return

# this route is what is called when adding a recon service in openrefine
@app.route("/reconcile/mads", methods=["POST", "GET"])
def reconcile():
    queries = request.form.get('queries')
    # if content in queries (i.e. names), deserialize the content
    if queries: 
        # loads returns a dict
        queries = json.loads(queries)
        results = {}
        # iterates through the dict, gets the key? not sure what type is. 
        for (key, query) in queries.items():
            qtype = query.get('type')
            if qtype is None:
                return jsonpify(metadata)
            limit = 3
            if 'limit' in query:
                limit = int(query['limit'])
            data = search(query['query'], query_type=qtype, limit=limit)
            #print(query['query'])
            results[key] = {"result": data}
        return jsonpify(results)
    return jsonpify(metadata)

if __name__ == "__main__":
    # defaults to localhost port 5000
    # http://127.0.0.1:5000/reconcile/mads
    app.run(debug=True)
