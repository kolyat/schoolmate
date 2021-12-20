# Account


### API description

This application uses standard Django's API for authentication and user
management.

| Endpoint | Description |
| -------- | ----------- |
| `/profile/login/` | Log in |
| `/profile/logout/` | Log out |
| `/profile/password_reset/` | Password reset request |
| `/profile/password_reset/email/` | 'E-mail has been sent' message after password reset request |
| `/profile/password_reset/<uidb64>/<token>/` | New password setup interface |
| `/profile/password_reset/complete/` | Message after successful password setup |
| `/profile/password_change/` | Password change interface |
| `/profile/password_change/done/` | Endpoint for redirection after successful password change |

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

Retrieve user's info and settings.

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
    "birth_date": "2021-02-02",
    "email": "sam@school.edu",
    "school_form": "9B",
    "language": "ru",
    "skin": "contrast",
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
    ],
    "skins": [
        [
            "contrast",
            "Contrast"
        ],
        [
            "flat",
            "Flat"
        ],
        [
            "material",
            "Material"
        ]
    ]
}
```

#### Set user settings

Change settings of current user.

* **URL**:
`/profile/user/info/`

* **Method**:
`PATCH`
  
* **URL parameters**:
`none`

* **Data parameters**:
    * Required:
    `{'language': 'string', 'skin': 'string'}`

* **Success response**
    * Code: `202 ACCEPTED`

* **Error response**
    * Code: `400 BAD REQUEST`
 
##### Sample call

Request:
```
webix.ajax().patch(
    "/profile/user/info/",
    {"language": "de", "skin": "compact"}
);
```

Response data:
```json
{
    "username": "sam",
    "language": "de",
    "skin": "compact"
}
```
