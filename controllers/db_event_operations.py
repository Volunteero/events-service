import sys
from app import client, db, abort
from .json_controller import *
from .authorization_manager import is_allowed


# TODO: error handling
class MongoManageEvents:

    def __init__(self):
        self.events_col = db.events
        self.participation_col = db.participations

    def create(self, json_data, token):
        event = json_to_event(json_data)
        allowed = is_allowed(token, event['organization_id'], 'createEvent')

        if allowed:
            event_id = self.events_col.insert_one(event.__original__).inserted_id
            result = {'event_id': str(event_id)}
            return to_json(result)
        else:
            abort(401)

    def get_all(self):
        events_cursor = self.events_col.find()
        return cursor_to_json(events_cursor)

    def get_all_by(self, field, value):
        events_cursor = self.events_col.find({field: value})
        return cursor_to_json(events_cursor)

    def get_by_id(self, id):
        event = self.events_col.find_one({"_id": ObjectId(id)})
        if event is not None:
            return to_json(format_ObjectId(event))
        else:
            abort(404)

    def archive(self, id, token):
        event = self.events_col.find_one({"_id": ObjectId(id)})
        if event is None:
            abort(404)

        allowed = is_allowed(token, event['organization_id'], 'closeEvent')
        if allowed:
            self.events_col.update_one({'_id': ObjectId(id)}, {"$set": {"available": False}}, upsert=True)
            return self.get_by_id(id)
        else:
            abort(401)

    def update(self, id, field, value, token):
        event = self.events_col.find_one({"_id": ObjectId(id)})
        if event is None:
            abort(404)
        # TODO: set correct action
        allowed = is_allowed(token, event['organization_id'], 'setNumberOfEventPoints')

        # TODO: validate with the Event obj
        if allowed:
            self.events_col.update_one({'_id': ObjectId(id)}, {"$set": {field: value}}, upsert=True)
            return self.get_by_id(id)
        else:
            abort(401)

    def update_event_participants(self, event_id):
        participants = self.participation_col.find_one({"event_id": event_id})['enrolled_participants']
        nr_participants = len(participants)
        self.events_col.update_one({'_id': ObjectId(event_id)}, {"$set": {"volunteers": nr_participants}}, upsert=True)
