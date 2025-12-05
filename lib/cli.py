import click
from lib.helpers import get_session, engine, Base
from lib.models.user import User
from lib.models.task import Task
from lib.seed import seed_data

@click.group()
def cli():
    pass

@cli.command("init-db")
def init_db():
    Base.metadata.create_all(engine)
    click.echo("Database initialized.")

@cli.command("seed")
def seed():
    seed_data()
    click.echo("Seed data added.")

@cli.command("create-user")
@click.argument("username")
def create_user(username):
    session = get_session()
    try:
        if session.query(User).filter_by(username=username).first():
            click.echo("User exists.")
            return
        user = User(username=username)
        session.add(user)
        session.commit()
        click.echo(f"User {username} created.")
    finally:
        session.close()

@cli.command("add-task")
@click.argument("username")
@click.argument("title")
@click.option("--description", "-d", default="")
@click.option("--priority", "-p", default=3)
def add_task(username, title, description, priority):
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            click.echo("User not found.")
            return
        task = Task(title=title, description=description, priority=priority, owner=user)
        session.add(task)
        session.commit()
        click.echo(f"Task '{title}' added for {username}.")
    finally:
        session.close()

@cli.command("list-tasks")
@click.argument("username")
def list_tasks(username):
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user or not user.tasks:
            click.echo("No tasks found.")
            return
        for t in user.tasks:
            status = "x" if t.completed else " "
            click.echo(f"[{status}] {t.id}: {t.title} (priority={t.priority})")
    finally:
        session.close()

@cli.command("complete-task")
@click.argument("task_id", type=int)
def complete_task(task_id):
    session = get_session()
    try:
        task = session.query(Task).get(task_id)
        if not task:
            click.echo("Task not found.")
            return
        task.completed = True
        session.commit()
        click.echo(f"Task {task_id} completed.")
    finally:
        session.close()

if __name__ == "__main__":
    cli()
