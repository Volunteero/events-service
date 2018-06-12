import sys
from app import app
from controllers.db_event_operations import MongoManageEvents
from controllers.db_participation_operations import MongoManageParticipations

mongo_events = MongoManageEvents()
mongo_participations = MongoManageParticipations()


@app.route("/")
def hello():
    return "Hello, welcome! Event-service is up and ready"

# import events and participation api endpoints
import api.api_events, api.api_participation



