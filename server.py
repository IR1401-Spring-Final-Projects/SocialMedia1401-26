from flask import Flask, request
from flask import jsonify

from hw3 import models

app = Flask(__name__)


@app.route("/hw3/models")
def list_models():
    return jsonify([model.__class__.__name__ for model in models])


def find_model(model_name):
    for model in models:
        if model.__class__.__name__ == model_name:
            return model
    return None


@app.route("/hw3/query", methods=['GET'])
def query_model():
    query = request.args.get("query")
    model_name = request.args.get("model_name")
    print(f"query_model> '{query}'")
    print(f"model_name> '{model_name}'")

    model = find_model(model_name)
    results = model.search(10, query)
    return results.to_json(orient="records")
