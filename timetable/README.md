# Timetable


### API description

#### Get timetable

* **URL**:
`/data/`

* **Method**:
`GET`
  
* **URL parameters**:
    * Required:
    `form_number=[integer]` (0 - get whole timetable for all school forms)

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`
 
* **Error response**:
    * Code: `404 PAGE NOT FOUND` if `form_number` less than zero or not integer

##### Sample call

Request:
```
webix.ajax().get(
    "/data/9",
    {}
);
```

Response data:
```json
[
    {
        "form_number": 9,
        "form_letter": "A",
        "lessons": [
            {
                "day_of_week": 2,
                "lesson_number": 1,
                "subject": "Algebra",
                "classroom": "1"
            },
            {
                "day_of_week": 2,
                "lesson_number": 2,
                "subject": "Physics",
                "classroom": "2"
            }
        ]
    },
    {
        "form_number": 9,
        "form_letter": "B",
        "lessons": [
            {
                "day_of_week": 2,
                "lesson_number": 1,
                "subject": "P.E.",
                "classroom": ""
            }
        ]
    }
]
```
