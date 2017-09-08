import datetime

import click
import faker
from flask.cli import AppGroup

from .extensions import db
from .models import Task


@click.group(cls=AppGroup)
def tasks():
    """Manage tasks."""


@tasks.command()
@click.argument('n', type=int, nargs=1)
@click.option('--seed', type=int)
def generate(n, seed):
    """Generate N random tasks."""
    fake = faker.Faker()
    fake.seed_instance(seed)
    for _ in range(n):
        task = Task(
            id=fake.uuid4(),
            title=fake.sentence(nb_words=4, variable_nb_words=True),
            is_completed=fake.boolean(),
            created_at=fake.date_time_between_dates(
                datetime_start=datetime.datetime(2016, 1, 1),
                datetime_end=datetime.datetime(2017, 6, 1),
                tzinfo=None
            )
        )
        print(task)
        db.session.add(task)
    db.session.commit()


@tasks.command()
def delete():
    """Delete all tasks."""
    db.session.query(Task).delete()
    db.session.commit()
