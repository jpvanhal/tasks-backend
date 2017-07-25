from marshmallow import ValidationError, validate, validates
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


class TaskSchema(Schema):
    id = fields.UUID()
    title = fields.Str(required=True, validate=validate.Length(min=1))
    is_completed = fields.Boolean()
    created_at = fields.DateTime()

    class Meta:
        type_ = 'tasks'
        strict = True
        self_view = 'task_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'task_list'
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'

    @validates('title')
    def validate_title(self, data):
        if data != data.strip():
            raise ValidationError('Must not have leading or trailing whitespace.')
