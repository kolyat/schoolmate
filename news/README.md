# News


### API description

#### Get news

Retrieve list of news (latest 300 articles by default).<br>
Number of articles is set in `LATEST_NEWS_COUNT` in project's `settings.py`

* **URL**:
`/news/`

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
    "/news/",
    {}
);
```

Response data:
```json
[
    {
        "created": "2020-02-18",
        "title": "Title 1",
        "content": "Content 1",
        "author": null
    },
    {
        "created": "2020-02-17",
        "title": "Title 2",
        "content": "Content 2",
        "author": "sam"
    }
]
```
