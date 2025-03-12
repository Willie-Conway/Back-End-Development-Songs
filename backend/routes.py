from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))

# client = MongoClient(
#     f"mongodb://{app.config['MONGO_USERNAME']}:{app.config['MONGO_PASSWORD']}@localhost")
mongodb_service = os.environ.get('MONGODB_SERVICE')
mongodb_username = os.environ.get('MONGODB_USERNAME')
mongodb_password = os.environ.get('MONGODB_PASSWORD')
mongodb_port = os.environ.get('MONGODB_PORT')

print(f'The value of MONGODB_SERVICE is: {mongodb_service}')

if mongodb_service == None:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    # abort(500, 'Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)

if mongodb_username and mongodb_password:
    url = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}"
else:
    url = f"mongodb://{mongodb_service}"


print(f"connecting to url: {url}")

try:
    client = MongoClient(url)
except OperationFailure as e:
    app.logger.error(f"Authentication error: {str(e)}")

db = client.songs
db.songs.drop()
db.songs.insert_many(songs_list)

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# INSERT CODE HERE
######################################################################

######################################################################
# Implement the /health endpoint
######################################################################
@app.route("/health", methods=["GET"])
def healthz():
    """Health check endpoint"""
    return jsonify({"status": "OK"}), 200

######################################################################
# Implement the /count endpoint
######################################################################
@app.route("/count", methods=["GET"])
def count():
    """Return the number of songs in the database"""
    count = db.songs.count_documents({})
    return jsonify({"count": count}), 200

######################################################################
# Implement the GET /song endpoint
######################################################################
@app.route("/song", methods=["GET"])
def songs():
    """Get all songs from the database"""
    results = list(db.songs.find({}))  # Retrieve all songs from the database
    return jsonify({"songs": parse_json(results)}), 200

######################################################################
# Implement the GET /song/<id> endpoint
######################################################################
@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    """Get a specific song by its ID."""
    song = db.songs.find_one({"id": id})

    if song is None:
        return jsonify({"message": f"song with id {id} not found"}), 404

    return jsonify(parse_json(song)), 200


