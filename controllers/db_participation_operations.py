import sys
from app import client, db
from .json_controller import *
from .db_event_operations import MongoManageEvents

event_manager = MongoManageEvents()


# TODO: error handling
class MongoManageParticipations:

    def __init__(self):
        self.events_col = db.events
        self.participation_col = db.participations

    def get_participators(self, event_id):
        # get participators of given event
        if event_id is not None:
            participations = self.participation_col.find_one({"event_id": event_id})
            return to_json(format_ObjectId(participations))
        # get all participators for all events
        else:
            participation_cursor = self.participation_col.find()
            return cursor_to_json(participation_cursor)

    def join(self, event_id, user_id):
        self.participation_col.update_one(
            {'event_id': event_id},
            {'$addToSet': {'participators': user_id}},
            upsert=True
        )

        # set nr of volunteers on event level
        event_manager.update_event_participators(event_id)
        return self.get_participators(event_id)

    def leave(self, event_id, user_id):
        self.participation_col.update_one(
            {'event_id': event_id},
            {'$pull': {'participators': user_id}}
        )

        # set nr of volunteers on event level
        event_manager.update_event_participators(event_id)
        return self.get_participators(event_id)

    def get_user_events(self, user_id):
        user_events = self.participation_col.find({'participators': {"$in": [user_id]}})

        # only return array of event ids
        events_arr = []
        for event in user_events:
            events_arr.append(event['event_id'])
        return to_json(events_arr)



