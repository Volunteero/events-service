import sys
from flask import Flask, request
from event_service.app import app
from .database_controller import MongoDBManager
mongodb = MongoDBManager()

@app.route("/")
def hello():
    return "event-service is running"

@app.route("/events", methods=['POST'])
def create_event():
    data = request.get_json()
    return mongodb.create(data)

@app.route("/events", methods=['GET'])
def get_all():
    return mongodb.get_all()

@app.route("/events/find", methods=['POST'])
def get_all_by():
    data = request.get_json()
    return mongodb.get_all_by(data['field'], data['value'])

@app.route("/events/<id>" , methods=['GET'])
def get_by_id(id):
    return mongodb.get_by_id(id)

@app.route("/events/<id>" , methods=['PATCH'])
def archive(id):
    return mongodb.archive(id)

@app.route("/events/<id>" , methods=['PUT'])
def update(id):
    data = request.get_json()
    return mongodb.update(id, data['field'], data['value'])
