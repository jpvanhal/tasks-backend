import datetime
import json

import pytest
from flask import Response
from werkzeug import cached_property

from tasks.app import create_app
from tasks.extensions import db
from tasks.models import Task


class JsonResponse(Response):
    @cached_property
    def json(self):
        return json.loads(self.data)


@pytest.fixture
def app(monkeypatch):
    app = create_app(
        DEBUG=True,
        SQLALCHEMY_DATABASE_URI='postgres://localhost/tasks_test',
        TESTING=True,
    )
    app.response_class = JsonResponse
    with app.app_context():
        try:
            db.create_all()
            yield app
        finally:
            db.session.remove()
            db.session.close_all()
            db.engine.dispose()
            db.drop_all()


@pytest.fixture
def tasks(app):
    tasks = [
        Task(
            id='93c15d1a-7ef7-4230-9937-2d083710b9a5',
            title='Buy groceries',
            is_completed=True,
            created_at=datetime.datetime(2017, 7, 4, 10, 55, 0),
        ),
        Task(
            id='6616a883-4ae1-408e-8eee-59699236191e',
            title='Plan trip to Lisbon',
            is_completed=False,
            created_at=datetime.datetime(2017, 5, 13, 20, 18, 0),
        ),
        Task(
            id='47446e2f-25d5-4672-bdd4-8313fdf8c033',
            title='Finish thesis',
            is_completed=False,
            created_at=datetime.datetime(2017, 1, 18, 9, 30, 0),
        ),
        Task(
            id='51a69ff0-2e25-4b69-8073-07a4d59076ef',
            title='Watch Alien: Covenant',
            is_completed=False,
            created_at=datetime.datetime(2017, 5, 17, 21, 32, 0),
        ),
    ]
    db.session.add_all(tasks)
    db.session.commit()
    return tasks


@pytest.fixture
def client(app):
    return app.test_client()


def test_list_tasks(client, tasks):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json['data']) == 4


def test_get_task(client, tasks):
    response = client.get('/tasks/6616a883-4ae1-408e-8eee-59699236191e')
    assert response.status_code == 200
    assert response.json == {
        'data': {
            'type': 'tasks',
            'id': '6616a883-4ae1-408e-8eee-59699236191e',
            'attributes': {
                'title': 'Plan trip to Lisbon',
                'is_completed': False,
                'created_at': '2017-05-13T20:18:00.000000Z',
            },
            'links': {
                'self': '/tasks/6616a883-4ae1-408e-8eee-59699236191e',
            },
        },
        'links': {
            'self': '/tasks/6616a883-4ae1-408e-8eee-59699236191e',
        },
        'jsonapi': {
            'version': '1.0',
        },
    }


def test_get_task_not_found(client, tasks):
    response = client.get('/tasks/2aa998e7-259d-4214-a97a-ef664c5ba8d4')
    assert response.status_code == 404


def test_create_task(client):
    response = client.post(
        '/tasks',
        content_type='application/vnd.api+json',
        data=json.dumps({
            'data': {
                'type': 'tasks',
                'id': '2aa998e7-259d-4214-a97a-ef664c5ba8d4',
                'attributes': {
                    'title': 'Implement the backend',
                    'is_completed': False,
                    'created_at': '2017-01-01T00:00:00.000000Z',
                },
            },
        })
    )
    assert response.status_code == 201
    assert response.json['data']['id'] == '2aa998e7-259d-4214-a97a-ef664c5ba8d4'
    assert response.json['data']['attributes']['title'] == 'Implement the backend'
    assert response.json['data']['attributes']['created_at'] == '2017-01-01T00:00:00.000000Z'


@pytest.mark.parametrize('data', [
    {'type': 'tasks', 'attributes': {}},
    {'type': 'tasks', 'attributes': {'title': None}},
    {'type': 'tasks', 'attributes': {'title': ''}},
    {'type': 'tasks', 'attributes': {'title': '   '}},
    {'type': 'tasks', 'id': 'invalid', 'attributes': {'title': 'Just do it!'}},
])
def test_create_task_invalid(client, data, tasks):
    response = client.post(
        '/tasks',
        content_type='application/vnd.api+json',
        data=json.dumps({'data': data}),
    )
    assert response.status_code == 422


@pytest.mark.xfail
def test_create_task_conflict(client, tasks):
    response = client.post(
        '/tasks',
        content_type='application/vnd.api+json',
        data=json.dumps({
            'data': {
                'type': 'tasks',
                'id': '6616a883-4ae1-408e-8eee-59699236191e',
                'attributes': {
                    'title': 'Just do it!'
                }
            },
        }),
    )
    assert response.status_code == 409


def test_delete_task(client, tasks):
    response = client.delete('/tasks/6616a883-4ae1-408e-8eee-59699236191e')
    assert response.status_code == 200


def test_delete_task_not_found(client, tasks):
    response = client.delete('/tasks/2aa998e7-259d-4214-a97a-ef664c5ba8d4')
    assert response.status_code == 404


@pytest.mark.parametrize('attributes', [
    {'title': 'Plan trip to Portugal'},
    {'is_completed': True},
])
def test_patch_task(client, tasks, attributes):
    response = client.patch(
        '/tasks/6616a883-4ae1-408e-8eee-59699236191e',
        content_type='application/vnd.api+json',
        data=json.dumps({
            'data': {
                'type': 'tasks',
                'id': '6616a883-4ae1-408e-8eee-59699236191e',
                'attributes': attributes,
            }
        })
    )
    assert response.status_code == 200
