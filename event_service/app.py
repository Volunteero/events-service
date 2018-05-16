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

import event_service.controllers.event_controller