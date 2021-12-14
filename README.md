# Schoolmate

**Schoolmate** is a school management software designed to automate a school's 
diverse operations from classes to school events. This management system 
contains various features to effectively record, manage and process data, and
consists of the following modules:

* **School** application describes, in general, model of a school: its inner 
structure, study hours, school year, etc. This application is mandatory.

* **Account** provides authentication and user's profile management. Uses
standard Django's components for this purpose.

* **News**. This application manages news articles that are displayed on main
page.

* **Timetable** app is used for structuring timetable of a school year.

* **Diary** app represents diary of a school student, it stores student's
everyday records as well as personal adjustments in timetable.

##### Application dependencies

* `school`: no dependencies
* `account`: `school`
* `news`: `account`
* `timetable`: `school`
* `diary`: `school`, `account`, `timetable`

##### Supported languages

* English
* Deutsch
* Русский

### Requirements

- Python 3.8 or higher
- Database management system: 
    - SQLite (not recommended)
    - PostgreSQL 9.6 or higher
- Packages listed in `requirements.txt`
- _Optional:_ mail server

### Testing deployment

1. If you're planning to use PostgreSQL, be sure, that the directory containing
   `pg_config` is included to the `PATH` variable.

2. Clone schoolmate repository:
    ```bash
    git clone https://github.com/kolyat/schoolmate.git
    cd schoolmate
    ```

3. Create virtual environment for project and activate it (for more information
   visit [this](https://docs.python-guide.org/dev/virtualenvs/) guide):
    ```bash
    virtualenv -p /usr/bin/python3.8 venv
    source venv/bin/activate
    ```

4. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

5. Open `./schoolmate/settings.py` and set up the project:
   1. Update `SECRET_KEY` if necessary.
   2. Set `DEBUG = True` for debugging mode.
   3. Configure database connection in `DATABASES` section.
   4. _Optional_: configure interaction with mail server.
   5. _Optional_: include password validators if necessary in 
      `AUTH_PASSWORD_VALIDATORS` variable.
   6. Select preferable locale in `LANGUAGE_CODE` and configure `TIME_ZONE`.
      More about time zones 
      [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
   7. _Optional_: set up number of articles that will be loaded by client in 
      `LATEST_NEWS_COUNT` variable.

6. Run `prepare_db.py` in order to create database and it's structure.

7. Create superuser:
    ```bash
    manage.py createsuperuser
    ```

8. Run development server with
    ```bash
    manage.py runserver
    ```

9. Do not forget to deactivate virtual environment after server shutdown if
   `venv` is not needed anymore:
    ```bash
    deactivate
    ```
