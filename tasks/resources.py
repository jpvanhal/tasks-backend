from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from .extensions import db
from .models import Task
from .schemas import TaskSchema


class TaskList(ResourceList):
    schema = TaskSchema
    data_layer = {
        'session': db.session,
        'model': Task,
    }


class TaskDetail(ResourceDetail):
    schema = TaskSchema
    data_layer = {
        'session': db.session,
        'model': Task,
    }

    def after_get(self, result):
        if result['data'] is None:
            raise ObjectNotFound(detail='', source={})
