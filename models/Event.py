import warlock
from jsonschema import validate

#https://github.com/bcwaldon/warlock
schema = {
    'name': 'Event',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'category': {'type': 'string'},
        'location': {'type': 'string'},
        'start': {'type': 'string'},
        'end': {'type': 'string'},
        'volunteers': {'type': 'integer'},
        'points': {'type': 'integer'},
        'organization_id': {'type': 'string'},
        'available': {'type': 'boolean'},
    },
    'additionalProperties': True,
}

Event = warlock.model_factory(schema)



