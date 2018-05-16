import os, sys
from pymongo import MongoClient
from flask import Flask, request
from bson.objectid import ObjectId
import json
from bson import json_util
app = Flask(__name__)

# connect to mongodb
MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = os.environ.get('MONGO_URL_DEV')

client = MongoClient(MONGO_URL)
db = client.get_default_database()

import controllers.event_controller

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)