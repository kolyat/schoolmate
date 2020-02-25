# Diary


### API description

#### Get records

Retrieve diary records with timetable for specified date

* **URL**:
`/diary/<int:year>/<int:month>/<int:day>/`

* **Method**:
`GET`
  
* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`

* **Error response**
    * Code: `424 FAILED DEPENDENCY` if current user is not assigned to any
            of school forms<br>
      Content: `{ "error": "Current user is not assigned to any of school forms" }`
 
##### Sample call

Request:
```
webix.ajax().get(
    "/diary/2019/02/29/",
    {}
);
```

Response data:
```json
[
    {
        "id": 1,
        "lesson_num": 1,
        "subject": "Algebra",
        "record": "Some records here",
        "marks": "",
        "signature": ""
    },
    {
        "id": 2,
        "lesson_num": 2,
        "subject": "Physics",
        "marks": "",
        "signature": ""
    },
    {
        "id": 3,
        "lesson_num": 3,
        "subject": "Chemistry",
        "record": "Some records here",
        "marks": "",
        "signature": ""
    },
    {
        "id": 4,
        "lesson_num": 4,
        "subject": "Biology",
        "marks": "",
        "signature": ""
    },
    {
        "id": 5,
        "lesson_num": 5,
        "subject": "P.E.",
        "marks": "",
        "signature": ""
    },
    {
        "id": 6,
        "lesson_num": 6,
        "subject": "",
        "marks": "",
        "signature": ""
    },
    {
        "id": 7,
        "lesson_num": 7,
        "subject": "",
        "marks": "",
        "signature": ""
    }
]
```

#### Create/update record

* **URL**:
`/diary/<int:year>/<int:month>/<int:day>/`

* **Method**:
`POST`
  
* **URL parameters**:
`none`

* **Data parameters**:
    * Required:<br>
        `lesson_number: integer`<br>
        `subject: string`<br>
        `text: string`

* **Success response**
    * Code: `201 CREATED` - new record
    * Code: `202 ACCEPTED` - update existing record

* **Error response**
    * Code: `400 BAD REQUEST`<br>
      Content: `{ "subject": "Given school subject does not exist" }`
 
##### Sample call

Request:
```
webix.ajax().post(
    "/diary/2019/02/29/",
    {
        "lesson_number": 3,
        "subject": "Chemistry",
        "text": "New records here"
    }
);
```

Response data:
```json
{
    "date": "2020-02-29",
    "lesson_number": 3,
    "subject": "Chemistry",
    "text": "New records here"
}
```
