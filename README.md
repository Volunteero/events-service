# events-service

Takes care of Volunteero's event-related operations. Events-service is implemented with Python and MongoDB.

## How to use?

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
Output for 2 events:
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

POST **/events/find** </br>
Gets all events that match the given criteria in request body, can be used for any property (name, category, available, points, ...)
```
Input example:
{
	"field":"available",
	"value":true
}

Output:
Outputs all events that match the criteria in the same format as GET /events (above).
```

GET **/events/id** </br>
Returns an event with the given event id.
```
Output
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

POST **/events** </br>
Creates a new event based on content, returns newly created event-id when successful
```
Input example:
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

Output example:
000000000000000000000000
```

### Delete (archive) event

PATCH **/events/id** </br>
Archives an event with the given event id. Used instead of deletion to keep the data. Returns the changed event.
```
Output
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

PUT **/events/id** </br>
Updates an event with the given event id (in URL path), based on the field and value sent in request. Returns the changed event.
```
Input example (in body):
{
  "field": "name",
  "value":"This is my new name",
}

Output
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

### Local Deployment
coming