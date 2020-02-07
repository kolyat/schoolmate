# Timetable


### API description

|       |       |
| ----- | ----- |
| Title | Get timetable |
| URL | /data/ |
| Method | GET |
| URL parameters | None |
| Data parameters | **Optional:**<br>form_number: integer |
| Success response | Code: 200 OK |
| Error Response |       |
| Notes |       |

##### Sample call

Request:
```
webix.ajax().get(
    "/data/",
    {
        form_number: 9
    }
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
            },
            ...
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
            },
            ...
        ]
    }
]
```
