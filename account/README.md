# Account


### API description

This application uses standard Django's API for authentication and user
management.

- `/profile/login/`
- `/profile/logout/`
- `/profile/password_reset/`
- `/profile/password_reset/sent/`
- `/profile/password_reset/<uidb64>/<token>/`
- `/profile/password_reset/complete/`
- `/profile/password_change/`
- `/profile/password_change/done/`

See [official Django documentation](https://docs.djangoproject.com/en/2.0/topics/auth/)
for further details.

### Custom API

#### Get username

Retrieve username of currently logged in user.

* **URL**:
`/profile/user/`

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
    "/profile/user/",
    {}
);
```

Response data:
```json
{
    "username": "sam"
}
```

#### Get user info

Retrieves user info and available system languages.

* **URL**:
`/profile/user/info/`

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
    "/profile/user/info/",
    {}
);
```

Response data:
```json
{
    "username": "sam",
    "first_name": "Sam",
    "last_name": "Smith",
    "patronymic_name": "J.",
    "birth_date": "2020-02-02",
    "email": "sam@school.edu",
    "school_form": "9B",
    "language": "ru",
    "languages": [
        [
            "ru",
            "Русский"
        ],
        [
            "en",
            "English"
        ],
        [
            "de",
            "Deutsch"
        ]
    ]
}
```
