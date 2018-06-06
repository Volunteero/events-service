import sys
import json
from bson import json_util, ObjectId
from models.Event import Event


# convert mongodb to json
def to_json(data):
    return json.dumps(data, default=json_util.default, indent=2, sort_keys=True)


def json_to_event(data):
    try:
        return Event(
            name=data['name'],
            description=data['description'],
            category=data['category'],
            location=data['location'],
            start=data['start'],
            end=data['end'],
            volunteers=data['volunteers'],
            points=data['points'],
            organization_id=data['organization_id'],
            available=True
        )
    except Exception as e:
        print(getattr(e, 'message', str(e)))
        raise e


def format_ObjectId(event):
    event['_id'] = str(event['_id'])
    return event
