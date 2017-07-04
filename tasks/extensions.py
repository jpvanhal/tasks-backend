from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@db.event.listens_for(db.metadata, 'before_create')
def create_postgres_extensions(target, connection, **kw):
    connection.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
