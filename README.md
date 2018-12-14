# GIZ Projects

# Local development

1. Clone this repo
2. Create a python virtual environment. ```virtualenv <env_name>```
3. Activate virtual environment ``` source <env_name>/bin/activate```
4. Install dependencies.

   Some python packages require system packages.
   * psycopg2 requires libpq-dev (postgresql development files).
   * shapely requires libgeos-dev (Geometry engine development files).
   * gnureadline requires libncurses5-dev (ncurses development files).
   * multiple packages require python development files (python-dev).

   After these packages have being installed the python packages can then be installed. ```pip install -r requiments.txt```
5. Install postgresql and create a user and a database.

   ``createuser giz -W``

   * -W will prompt to create a password for the user.

   ``createdb giz -O giz``

   * -O will give ownership of the database to the municipal_finance user.

5. Run migrations
    ``python manage.py migrate``

6. Load data from fixtures
    ``python manage.py loaddata scorecard/fixtures/initial_data.json``


7. run it: ``python manage.py runserver``

Note when doing a high request rate locally e.g. during updates, it seems that the above command doesn't release resources quickly enough so use the following for the API server instead

```bash
export DJANGO_SETTINGS_MODULE=scorecard.settings
export API_URL=http://localhost:8001/api  # only needed if using the table view against local API
export PRELOAD_CUBES=true
export SITE_ID=3
gunicorn --limit-request-line 7168 --worker-class gevent municipal_finance.wsgi:application -t 600 --log-file -
```

# Production

```
dokku config:set giz DJANGO_DEBUG=False \
                     DISABLE_COLLECTSTATIC=1 \
                     DJANGO_SECRET_KEY=... \
                     NEW_RELIC_APP_NAME=municipal_finance \
                     NEW_RELIC_LICENSE_KEY=... \
                     DATABASE_URL=postgres://giz:...@postgresq....amazonaws.com/giz
```
