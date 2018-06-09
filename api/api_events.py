import sys
from flask import request
from api.api_global import mongo_events, app


@app.route("/events", methods=['POST'])
def create_event():
    data = request.get_json()
    token = request.args.get('token')
    return mongo_events.create(data, token)


@app.route("/events", methods=['GET'])
def get_events():
    return mongo_events.get_all()


@app.route("/events/by", methods=['POST'])
def get_events_by():
    data = request.get_json()
    return mongo_events.get_all_by(data['field'], data['value'])


@app.route("/events/<id>", methods=['GET'])
def get_event_by_id(id):
    return mongo_events.get_by_id(id)


@app.route("/events/<id>", methods=['DELETE'])
def archive_event(id):
    token = request.args.get('token')
    return mongo_events.archive(id, token)


@app.route("/events/<id>", methods=['PUT'])
def update_event(id):
    token = request.args.get('token')
    data = request.get_json()
    return mongo_events.update(id, data['field'], data['value'], token)
