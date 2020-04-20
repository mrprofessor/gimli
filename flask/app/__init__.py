from flask import Flask, request
from flask_pymongo import PyMongo
from bson.json_util import dumps


app = Flask(__name__)
app.config["MONGO_URI"] = (
    "mongodb://user_one:test_user_one1@ds133256.mlab.com:33256/gimli"
    + "?retryWrites=false"
)
mongo_client = PyMongo(app)


# Create seed data
# urls.insert_many(SEED_DATA)

urls = mongo_client.db["urls"]


@app.route("/url", methods=["GET"])
def list():
    search_key = request.args.get("search")

    # List all the urls
    if not search_key:
        return dumps(urls.find())

    urls.create_index([("long_url", "text")])
    data = urls.find({"$text": {"$search": search_key}})

    return dumps(data)


@app.route("/url", methods=["POST"])
def post():
    long_url = request.json.get("url")
    # FIXME add better error messages
    if not long_url:
        return "No URL found"

    # build data
    url_object = build_url_object(long_url)
    data = urls.insert_one(url_object)
    result = urls.find_one({"_id": data.inserted_id})
    return dumps(result)


@app.route("/url/<short_url_key>", methods=["get"])
def get(short_url_key):
    return short_url_key


# ----------------------------
# UTILS
# ----------------------------
def build_url_object(long_url):
    # Hard-coded for now
    url_object = {
        "long_url": long_url,
        "short_url_key": "rdveser",
        "short_url": "https://localhost/rdveser",
        "total_traffic": 0,
        "hourly_traffic": 0,
    }

    return url_object
