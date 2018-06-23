import sys
import requests
from app import client, db, abort
from .json_controller import *
from .authorization_manager import is_allowed
from .external_services import *


# TODO: error handling
class MongoManageEvents:

    # error messages
    authorization_error = "Invalid access token, request unauthorized."
    event_not_found_error = "Event not found."
    event_created_organization_error = "Could not link event to organization. Event was not created."
    event_created_search_error = "Could not send event to search service. Event was created, " \
                                 "but cannot be found in the search service until added " \
                                 "to the search service again via update request."

    def __init__(self):
        self.events_col = db.events
        self.participation_col = db.participations

    def create(self, json_data, token):
        event = json_to_event(json_data)
        allowed = is_allowed(token, event['organization_id'], 'createEvent')

        if allowed:
            # add event
            event_id = str(self.events_col.insert_one(event.__original__).inserted_id)

            # link event to organization
            linking_to_organization = add_event_to_organization(event['organization_id'], event_id)
            if linking_to_organization.status_code > 299:
                self.events_col.remove({"_id": ObjectId(event_id)})
                abort(linking_to_organization.status_code, self.event_created_organization_error)  # or original content

            # send event to search service
            add_to_service = add_event_to_search(event, event_id)
            if add_to_service.status_code > 299:
                abort(add_to_service.status_code, self.event_created_search_error)  # or original content

            # if we are this far, everything is fine
            result = {'event_id': event_id}
            return to_json(result)
        else:
            abort(401, self.authorization_error)

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
            abort(404, self.event_not_found_error)

    def archive(self, id, token):
        event = self.events_col.find_one({"_id": ObjectId(id)})
        if event is None:
            abort(404, self.event_not_found_error)

        allowed = is_allowed(token, event['organization_id'], 'closeEvent')
        if allowed:
            self.events_col.update_one({'_id': ObjectId(id)}, {"$set": {"available": False}}, upsert=True)
            return self.get_by_id(id)
        else:
            abort(401, self.authorization_error)

    def update(self, id, field, value, token):
        event = self.events_col.find_one({"_id": ObjectId(id)})
        if event is None:
            abort(404, self.event_not_found_error)
        # TODO: set correct action
        allowed = is_allowed(token, event['organization_id'], 'setNumberOfEventPoints')

        # TODO: validate with the Event obj
        if allowed:
            self.events_col.update_one({'_id': ObjectId(id)}, {"$set": {field: value}}, upsert=True)
            return self.get_by_id(id)
        else:
            abort(401, self.authorization_error)


# lower: for participation and organization services
    def update_event_participants(self, event_id):
        participants = self.participation_col.find_one({"event_id": event_id})['enrolled_participants']
        nr_participants = len(participants)
        self.events_col.update_one({'_id': ObjectId(event_id)}, {"$set": {"volunteers": nr_participants}}, upsert=True)
        return


