import json
import requests


def is_allowed(token, organization_id, action):
    # send request
    url = 'https://volunteero-auth.herokuapp.com/auth/access'
    params = dict()
    params['accessToken'] = token
    params['resource'] = 'organisation:' + organization_id
    params['action'] = action
    response = requests.get(url, params=params)

    # get result
    allowed = False
    if response.status_code == 200:
        allowed = response.json()["allowed"]

    return allowed


# to test post call with events-service on Heroku
def test_post():
    new_url = 'https://volunteero-events.herokuapp.com/events'
    headers = {'Content-type': 'application/json'}
    body = {'name': 'new event',
            'description': 'my new event',
            'volunteers': 555,
            'location': 'my home',
            'start': '2018-01-02',
            'end': '2019-02-20',
            'category': 'food',
            'points': 2030,
            'organization_id': '0000000000000000000'
            }
    json_body = json.dumps(body)
    response = requests.post(new_url, data=json_body, headers=headers)
    return response.text

