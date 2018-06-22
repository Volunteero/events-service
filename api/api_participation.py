import sys
from flask import request
from api.api_global import mongo_participations, app


@app.route("/participation", methods=['GET'])
def get_participants():
    event = request.args.get('event')
    return mongo_participations.get_participants(event)


@app.route("/participation/user", methods=['GET'])
def get_user_events():
    user = request.args.get('user')
    return mongo_participations.get_user_events(user)


@app.route("/participation/arrived", methods=['GET'])
def get_if_user_participated():
    user = request.args.get('user')
    event = request.args.get('event')
    return mongo_participations.verify_if_arrived(event, user)


@app.route("/participation/arrived", methods=['POST'])
def sign_user_as_arrived():
    user = request.args.get('user')
    event = request.args.get('event')
    return mongo_participations.mark_as_arrived(event, user)


@app.route("/participation/enroll", methods=['POST'])
def enroll_in_event():
    data = request.get_json()
    return mongo_participations.enroll(data['event'], data['user'])


@app.route("/participation/leave", methods=['POST'])
def leave_an_event():
    data = request.get_json()
    return mongo_participations.leave(data['event'], data['user'])



