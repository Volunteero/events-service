import sys
from flask import request
from api.api_global import mongo_participations, app


@app.route("/participation", methods=['GET'])
def get_participators():
    event = request.args.get('event')
    return mongo_participations.get_participators(event)


@app.route("/participation/join", methods=['POST'])
def join_an_event():
    data = request.get_json()
    return mongo_participations.join(data['event'], data['user'])


@app.route("/participation/leave", methods=['POST'])
def leave_an_event():
    data = request.get_json()
    return mongo_participations.leave(data['event'], data['user'])


@app.route("/participation/user", methods=['GET'])
def get_user_events():
    user = request.args.get('user')
    return mongo_participations.get_user_events(user)
