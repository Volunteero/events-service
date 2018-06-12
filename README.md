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
Creates a new event based on content, returns newly created event-id when successful
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
000000000000000000000000
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
    "participators": [
      "user122",
      "user111"
    ]
  },
  {
    "_id": "0000000000000000000000xx",
    "event_id": "00000000000000000000000x",
    "participators": [
      "user112",
      "user111",
      "user113",
      "user114"
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
Gets a list of events (IDs) where user with the given ID participates.
```
Example output:
[
  "00000000000000000000000x",
  "00000000000000000000000y",
  "00000000000000000000000z",
  "00000000000000000000000c"
]
```

### Join events
POST **/participation/join** </br>
Let's user participate in a given event, based on event ID and user ID. Updates "volunteers" field of the event object itself as well.
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
Let's user leave/cancel participation in a given event, based on event ID and user ID. Updates "volunteers" field of the event object itself as well.
```
Input and output are the same as POST /participation/join.
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



