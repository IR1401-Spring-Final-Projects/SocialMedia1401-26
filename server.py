from flask import Flask, request
from flask import jsonify
from flask_cors import CORS

from clustering import find_cluster
from hw3 import models
from query_expansion import QueryExpander

app = Flask(__name__)
CORS(app)

qe = QueryExpander()


@app.route("/hw3/models")
def list_models():
    return jsonify([model.__class__.__name__ for model in models])


@app.route("/hw3/query", methods=['GET'])
def query_model():
    query = request.args.get("query")
    mode = request.args.get("mode")
    print(f"query_model> '{query}'")
    print(f"mode> '{mode}'")
    if mode and mode.isdigit():
        model = models[int(mode)]
    else:
        model = models[0]
    results = model.search(10, query)
    return results.to_json(orient="records")


@app.route("/clustering", methods=['GET'])
def clustering_api():
    query = request.args.get("query")
    print(f"query> '{query}'")
    return find_cluster(query)


@app.route("/qe", methods=['GET'])
def query_expander():
    query = request.args.get("query")
    print(f"query> '{query}'")
    return {"suggestions": qe.get_query_suggestions(query)}
