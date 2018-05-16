import sys
import warlock
from flask import Flask, request
from bson.objectid import ObjectId
from event_service.app import client, db
from .json_controller import *
from event_service.models.Event import Event

class MongoDBManager():

    def __init__(self):
        self.events_col = db.events

    def create(self, jsondata):
        try:
            event = json_to_event(jsondata)
            event_id = self.events_col.insert_one(event.__original__).inserted_id
            return str(event_id)
        except:
            print(str(sys.exc_info()[1]))
            return "Failed"

    def get_all(self):
        try:
            events_cursor = self.events_col.find()
            events_json = []
            for event in events_cursor:
                events_json.append(format_ObjectId(event))
            return to_json(events_json)
        except:
            print(str(sys.exc_info()[1]))
            return "Failed"

    def get_all_by(self, field, value):
        try:
            events_cursor = self.events_col.find({field: value})
            events_json = []
            for event in events_cursor:
                events_json.append(format_ObjectId(event))
            return to_json(events_json)
        except:
            print(str(sys.exc_info()[1]))
            return "Failed"

    def get_by_id(self, id):
        try:
            event = self.events_col.find_one({"_id": ObjectId(id)})
            return to_json(format_ObjectId(event))
        except:
            print(str(sys.exc_info()[1]))
            return "Failed"

    def archive(self, id):
        try:
            self.events_col.update_one({'_id': ObjectId(id)}, {"$set": {"available": False}}, upsert=True)
            return self.get_by_id(id)
        except:
            print(str(sys.exc_info()[1]))
            return "Failed"

    def update(self, id, field, value):
        try:
            # TODO: validate with the Event obj
            self.events_col.update_one({'_id': ObjectId(id)}, {"$set": {field: value}}, upsert=True)
            return self.get_by_id(id)
        except:
            print(str(sys.exc_info()[1]))
            return "Failed"
