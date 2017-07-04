import os

from flask import Flask
from flask_rest_jsonapi import Api


def create_app(**config):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/tasks_dev'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(config)
    if 'DATABASE_URL' in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    from .extensions import db
    db.init_app(app)

    from .resources import TaskDetail, TaskList
    api = Api(app)
    api.route(TaskList, 'task_list', '/tasks')
    api.route(TaskDetail, 'task_detail', '/tasks/<uuid:id>')

    return app
