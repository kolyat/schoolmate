# School


### API description

#### Get status

Retrieve server's date and time with period description

* **URL**:
`/main/status/`

* **Method**:
`GET`

* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`
 
##### Sample call

Request:
```
webix.ajax().get(
    "/main/status/",
    {}
);
```

Response data:
```json
{
    "date_description": [
        {
            "period_type": "Q",
            "description": "2nd semester"
        }
    ],
    "day": 25,
    "time_description": [
        {
            "description": "7th lesson"
        }
    ],
    "hour": 15,
    "month": 1,
    "second": 12,
    "minute": 33,
    "year": 2022
}
```


#### Get school forms

Retrieve list of school forms

* **URL**:
`/main/forms/`

* **Method**:
`GET`

* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`
 
##### Sample call

Request:
```
webix.ajax().get(
    "/main/forms/",
    {}
);
```

Response data:
```json
[
    {
        "number": 9,
        "letters": [
            "A",
            "B"
        ]
    },
    {
        "number": 11,
        "letters": [
            "A",
            "B"
        ]
    }
]
```


#### Get year's schedule

* **URL**:
`/main/schedule/year/`

* **Method**:
`GET`

* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`
 
##### Sample call

Request:
```
webix.ajax().get(
    "/main/schedule/year/",
    {}
);
```

Response data:
```json
[
    {
        "description": "2nd semester",
        "start_date": "2022-01-13",
        "end_date": "2022-05-25"
    },
    {
        "description": "Summer vacation",
        "start_date": "2022-05-26",
        "end_date": "2022-08-31"
    }
]
```


#### Get daily schedule

* **URL**:
`/main/schedule/day/`

* **Method**:
`GET`

* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`
 
##### Sample call

Request:
```
webix.ajax().get(
    "/main/schedule/day/",
    {}
);
```

Response data:
```json
[
    {
        "description": "1st lesson",
        "start_time": "09:00:00",
        "end_time": "09:45:00"
    },
    {
        "description": "1st break",
        "start_time": "09:45:01",
        "end_time": "09:55:00"
    }
]
```


#### Get school subjects

Retrieve list of school subjects

* **URL**:
`/main/subjects/`

* **Method**:
`GET`

* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`
 
##### Sample call

Request:
```
webix.ajax().get(
    "/main/subjects/",
    {}
);
```

Response data:
```json
[
    {
        "subject": "Biology"
    },
    {
        "subject": "Algebra"
    },
    {
        "subject": "P.E."
    }
]
```
