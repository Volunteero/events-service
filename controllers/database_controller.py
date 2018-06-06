import sys
from app import client, db
from .json_controller import *
from .authentication_manager import is_allowed


# TODO: error handling
class MongoDBManager:

    def __init__(self):
        self.events_col = db.events

    def create(self, json_data, token):
        event = json_to_event(json_data)
        allowed = is_allowed(token, event['organization_id'], 'createEvent')
        if allowed:
            event_id = self.events_col.insert_one(event.__original__).inserted_id
            return str(event_id)
        else:
            return "Failed to authorize"

    def get_all(self):
        events_cursor = self.events_col.find()
        events_json = []
        for event in events_cursor:
            events_json.append(format_ObjectId(event))
        return to_json(events_json)

    def get_all_by(self, field, value):
        events_cursor = self.events_col.find({field: value})
        events_json = []
        for event in events_cursor:
            events_json.append(format_ObjectId(event))
        return to_json(events_json)

    def get_by_id(self, id):
        event = self.events_col.find_one({"_id": ObjectId(id)})
        return to_json(format_ObjectId(event))

    def archive(self, id, token):
        event = self.events_col.find_one({"_id": ObjectId(id)})
        allowed = is_allowed(token, event['organization_id'], 'closeEvent')

        if allowed:
            self.events_col.update_one({'_id': ObjectId(id)}, {"$set": {"available": False}}, upsert=True)
            return self.get_by_id(id)
        else:
            return "Failed to authorize"

    def update(self, id, field, value, token):
        event = self.events_col.find_one({"_id": ObjectId(id)})
        # TODO: set correct action
        allowed = is_allowed(token, event['organization_id'], 'setNumberOfEventPoints')

        # TODO: validate with the Event obj
        if allowed:
            self.events_col.update_one({'_id': ObjectId(id)}, {"$set": {field: value}}, upsert=True)
            return self.get_by_id(id)
        else:
            return "Failed to authorize"
