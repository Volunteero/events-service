import os
from pymongo import MongoClient
from flask import Flask, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# connect to mongodb
MONGO_URL = os.environ.get('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.get_database()

# import api start point
import api.api_global

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
