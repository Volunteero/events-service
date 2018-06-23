import sys
from app import client, db, abort
from .json_controller import *
from .db_event_operations import MongoManageEvents
from .external_services import give_influence_points

event_manager = MongoManageEvents()


# TODO: error handling
class MongoManageParticipations:

    def __init__(self):
        self.events_col = db.events
        self.participation_col = db.participations

    def get_participants(self, event_id):
        # get participants of given event
        if event_id is not None:
            participations = self.participation_col.find_one({"event_id": event_id})
            if participations is not None:
                return to_json(format_ObjectId(participations))
            else:
                empty_result = {}
                empty_result['event_id'] = event_id
                empty_result['enrolled_participants'] = []
                empty_result['arrived_participants'] = []
                return to_json(empty_result)

        # get all participants for all events
        else:
            participation_cursor = self.participation_col.find()
            return cursor_to_json(participation_cursor)

    def enroll(self, event_id, user_id):
        self.participation_col.update_one(
            {'event_id': event_id},
            {'$addToSet': {'enrolled_participants': user_id}},
            upsert=True
        )

        # set nr of volunteers on event level
        event_manager.update_event_participants(event_id)
        return self.get_participants(event_id)

    def leave(self, event_id, user_id):
        self.participation_col.update_one(
            {'event_id': event_id},
            {'$pull': {'enrolled_participants': user_id}}
        )

        # set nr of volunteers on event level
        event_manager.update_event_participants(event_id)
        return self.get_participants(event_id)

    def get_user_events(self, user_id):
        user_event_ids = self.participation_col.find({'enrolled_participants': {"$in": [user_id]}})

        # only return array of event ids
        events_id_arr = []
        for event in user_event_ids:
            events_id_arr.append(event['event_id'])

        # for each id, get an event and append to array if event exists
        user_events = []
        for event_id in events_id_arr:
            event = self.events_col.find_one({'_id': ObjectId(event_id)})
            if event is not None:
                user_events.append(format_ObjectId(event))

        return to_json(user_events)


# verification methods of volunteer arriving to event
    def mark_as_arrived(self, event_id, user_id):
        self.participation_col.update_one(
            {'event_id': event_id},
            {'$addToSet': {'arrived_participants': user_id}},
            upsert=True
        )
        self.give_points(event_id, user_id)
        return self.get_participants(event_id)

    def verify_if_arrived(self, event_id, user_id):
        joined = self.participation_col.find_one(
            {"$and": [{'event_id': event_id}, {'enrolled_participants': {"$in": [user_id]}}]})
        appeared = self.participation_col.find_one(
            {"$and": [{'event_id': event_id}, {'arrived_participants': {"$in": [user_id]}}]})

        result = {'enrolled': bool(joined), 'arrived': bool(appeared)}
        return to_json(result)


# external method to call user service
    def give_points(self, event_id, user_id):
        event = self.events_col.find_one({"_id": ObjectId(event_id)})
        points = event['points']
        success = give_influence_points(points, user_id)
        if success.status_code > 299:
            if success.status_code < 500:
                abort(success.status_code, "Failed to give points to user, verify that user " + user_id + " exists.")
            else:
                abort(success.status_code, "Failed to give points to user.")
        return
