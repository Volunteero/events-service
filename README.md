# events-service

Takes care of Volunteero's event-related operations. Events-service is implemented with Python, Flask and MongoDB.
Find it on https://volunteero-events.herokuapp.com/

## How to use?

## Events

### General event format
- id: ObjectId('xxxxxxxxxxxxxxxxxxxxxxxx') is used internally in MongoDB. For retrieval, simple 'xxxxxxxxxxxxxxxxxxxxxxxx' is used.
- 'available' is used to avoid complete deletion of the event. By default, the value is set to true; when deleted (=archived), value is set to false.
```
{
  "_id": ObjectId('xxxxxxxxxxxxxxxxxxxxxxxx'),
  "name": string,
  "description": string,
  "start": string, -> possibly datetime
  "end": string,  -> possibly datetime
  "location": string,
  "volunteers": integer,
  "category": string,
  "points": integer,
  "organization_id": "xxxxxxxxxxxxxxxxxxxxxxxx",
  "available": true
}
```

### Retrieve events

GET **/events** </br>
Gets all events
```
Example output for 2 events:
[
  {
    "_id": "000000000000000000000000",
	"name":"Help to build a shelter",
	"description":"Come and lets build a shelter together!",
	"start":"2018-01-01",
	"end" : "2018-01-01",
	"location":"Berlin, Germany",
	"volunteers":100,
	"category":"building",
	"points":200,
	"organization_id":"000000000000000000000000",
	"available": true
  },
  {
     "_id": "000000000000000000000000",
	"name":"Help out in the soup kitchen",
	"description":"Spend your morning helping out with us!",
	"start":"2018-01-01",
	"end" : "2018-01-01",
	"location":"Bern, Switzerland",
	"volunteers":50,
	"category":"food",
	"points":100,
	"organization_id":"000000000000000000000000",
	"available": false
  }
]
```

POST **/events/by** </br>
Gets all events that match the given criteria in request body, can be used for any property (name, category, available, points, ...)
```
Example input:
{
	"field":"available",
	"value":true
}

Example output:
Outputs all events that match the criteria in the same format as GET /events (above).
```

GET **/events/<EVENT_ID>** </br>
Returns an event with the given event ID.
```
Example output
{
  "_id": "000000000000000000000000",
  "name":"Help to build a shelter",
  "description":"Come and lets build a shelter together!",
  "start":"2018-01-01",
  "end" : "2018-01-01",
  "location":"Berlin, Germany",
  "volunteers":100,
  "category":"building",
  "points":200,
  "organization_id":"000000000000000000000000",
  "available": true
}
```

### Create events

POST **/events?token=<ACCESS_TOKEN>** </br>
Creates a new event based on content, returns newly created event-id when successful. 
Adds also event to organization-service under given organization.
```
Example input:
{  
  "name":"Help to build a shelter",
  "description":"Come and lets build a shelter together!",
  "start":"2018-01-01",
  "end" : "2018-01-01",
  "location":"Berlin, Germany",
  "volunteers":100,
  "category":"building",
  "points":200,
  "organization_id":"000000000000000000000000"
}

Example output:
{
  "event_id":xxxxxxxxxxxxxxxxxxxxxxxx
}

Errors:
500 -> linking event to the organization failed
401 -> unauthorized (invalid or missing access token)
```

### Delete (archive) event

DELETE **/events/<EVENT_ID>?token=<ACCESS_TOKEN>** </br>
Archives an event with the given event ID. Used instead of deletion to keep the data. Returns the changed event.
```
Example output
{
  "_id": "000000000000000000000000",
  "name":"Help to build a shelter",
  "description":"Come and lets build a shelter together!",
  "start":"2018-01-01",
  "end" : "2018-01-01",
  "location":"Berlin, Germany",
  "volunteers":100,
  "category":"building",
  "points":200,
  "organization_id":"000000000000000000000000",
  "available": false
}

Errors:
404 -> event not found
401 -> unauthorized (invalid or missing access token)
```

### Update event

PUT **/events/<EVENT_ID>?token=<ACCESS_TOKEN>** </br>
Updates an event with the given event ID (in URL path), based on the field and value sent in request. Returns the changed event.
```
Example input (in body):
{
  "field": "name",
  "value":"This is my new name",
}

Example output
{
  "_id": "000000000000000000000000",
  "name":"This is my new name",
  "description":"Come and lets build a shelter together!",
  "start":"2018-01-01",
  "end" : "2018-01-01",
  "location":"Berlin, Germany",
  "volunteers":100,
  "category":"building",
  "points":200,
  "organization_id":"000000000000000000000000",
  "available": true
}

Errors:
404 -> event not found
401 -> unauthorized (invalid or missing access token)
```

## Participation


### Retrieve participations

GET **/participation** </br>
Gets all participating volunteers for all events
```
Example output for 2 events:
[
  {
    "_id": "0000000000000000000000yy",
    "event_id": "00000000000000000000000y",
    "enrolled_participants": [
      "user122",
      "user111"
    ],
    "arrived_participants": [
      "user122",
    ]
  },
  {
    "_id": "0000000000000000000000xx",
    "event_id": "00000000000000000000000x",
    "enrolled_participants": [
      "user112",
      "user133",
    ]
  }
]
```

GET **/participation?event=<EVENT_ID>** </br>
Gets all participating volunteers for this events
```
Outputs participators for one event, in the same format as GET /participation/ applies for one event.
```

GET **/participation/user?user=<USER_ID>** </br>
Gets a list of events where user with the given ID participates.
```
Outputs a list of events, same format as GET /events
```

### Join events
POST **/participation/enroll** </br>
Let's user enroll in a given event, based on event ID and user ID. Updates also "volunteers" field of the event object.
```
Example input:
{
	"event":"00000000000000000000000x",
	"user":"user1"
}

Outputs the updated event participation, in format of GET /participation?event=<EVENT_ID>.
```

### Leave events
POST **/participation/leave** </br>
Let's user leave/cancel participation in a given event, based on event ID and user ID. Updates also "volunteers" field of the event object.
```
Input and output are the same as POST /participation/enroll.
```


### Mark user as arrived (verify participation)
POST **/participation/arrived?event=<EVENT_ID>&user=<USER_ID>** </br>
Stores user arrival to the event.
```
Input body is empty, values are in the URL.

Outputs all participants of this event, like output of GET /participation?event=<EVENT_ID>.
```

### Gets user status for given event
GET **/participation/arrived?event=<EVENT_ID>&user=<USER_ID>** </br>
Gets if user has enrolled for the event, and if user arrived to the event.
```
Input body is empty, values are in the URL.

Example output:
{
  "arrived": true,
  "enrolled": true
}
```

## Setup

#### Virtualenv

If you don't have virtualenv installed: ( http://docs.python-guide.org/en/latest/dev/virtualenvs/ )
* ``pip install virtualenv``
* ``cd myprojectfolder``
* ``virtualenv myenv``

Activate virtualenv:
* ``"myenv/Scripts/activate"``

#### Set up project

Virtualenv must be activated latest at step 3

* ``git clone https://github.com/Volunteero/events-service.git``
* ``cd events-service``
* ``pip install -r requirements.txt``
* ``cd event_service``
* ``set FLASK_APP=app.py``
* ``set MONGO_URL=mongodb+srv://USER:PASSWORD@proepvolunteero-rvsmk.mongodb.net/DATABASE_NAME``
* ``flask run``



