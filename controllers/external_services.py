import json
import requests


# link an event to organization (when creation of new event)
def add_event_to_organization(organization_id, event_id):
    url = 'https://volunteero-organizations.herokuapp.com/organizations/add-event-to-organization/' + organization_id
    headers = {'Content-type': 'application/json'}
    body = {'event_id': event_id}
    json_body = json.dumps(body)
    response = requests.patch(url, data=json_body, headers=headers)
    return response


# send newly created event to search service
def add_new_event_to_search(event, event_id):
    # event is duplicated to add the id field (due to model constraint)
    event_body = {}
    event_body['name'] = event['name']
    event_body['description'] = event['description']
    event_body['start'] = event['start']
    event_body['end'] = event['end']
    event_body['location'] = event['location']
    event_body['volunteers'] = event['volunteers']
    event_body['category'] = event['category']
    event_body['points'] = event['points']
    event_body['organization_id'] = event['organization_id']
    event_body['id'] = event_id
    event_body['type'] = 'event'

    entities = [event_body]
    body = {'entities': entities}

    url = 'https://volunteero-search.herokuapp.com/api/v1/search/create'
    headers = {'Content-type': 'application/json'}
    json_body = json.dumps(body)
    response = requests.post(url, data=json_body, headers=headers)
    return response


# send updated event to search service
def add_updated_event_to_search(field, value, event_id):
    # event is duplicated to add the id field (due to model constraint)
    event_body = {}
    event_body[field] = value
    event_body['id'] = event_id
    event_body['type'] = 'event'

    entities = [event_body]
    body = {'entities': entities}

    url = 'https://volunteero-search.herokuapp.com/api/v1/search/update'
    headers = {'Content-type': 'application/json'}
    json_body = json.dumps(body)
    response = requests.post(url, data=json_body, headers=headers)
    return response