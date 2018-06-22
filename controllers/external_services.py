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
