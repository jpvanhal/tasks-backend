from sqlalchemy.dialects import postgresql

from .extensions import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        server_default=db.func.uuid_generate_v4(),
        nullable=False,
    )
    title = db.Column(db.Text, nullable=False)
    is_completed = db.Column(
        db.Boolean,
        server_default=db.false(),
        nullable=False
    )
    created_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=db.func.now()
    )

    def __str__(self):
        return '- [{check}] {title}'.format(
            check='X' if self.is_completed else ' ',
            title=self.title,
        )
