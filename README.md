# Tasks Backend

This is the server-side component for the offline-first application I implemented for my thesis. The server is a very basic API for task management. It follows the [JSON API specification](http://jsonapi.org).

## Requirements

* [Python 3.6](https://www.python.org)
* [Pipenv](https://docs.pipenv.org)
* [PostgreSQL](https://www.postgresql.org)

## Development

### Setting up the development environment

1. Create a virtualenv for the project:

       $ pipenv --python 3.6

2. Install the Python dependencies:

       $ pipenv install --dev

3. Activate the virtualenv:

       $ pipenv shell

4. Create the databases for development and testing:

       $ createdb tasks_dev
       $ createdb tasks_test

5. Run the database migrations for the development database:

       $ alembic upgrade head

6. Tell the Flask command-line client where the application can be found:

       $ export FLASK_APP=autoapp.py

   You might want to automate this using [direnv](https://direnv.net) or a similar tool.

### Running the development server

1. Start the development server:

       $ flask run

2. Open http://127.0.0.1:5000/ on your browser.

### Running the tests

You can run the tests with py.test:

    $ py.test

## Deploying

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
