import click
from lib.models.user import User
from lib.models.task import Task
from lib.models.base import Base, engine
from lib.helpers import get_session
from lib.seed import seed_data

@click.group()
def cli():
    """Personal Task Manager CLI"""
    pass

# -----------------------------
# Database Commands
# -----------------------------
@cli.command("init-db")
def init_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(engine)
    click.echo("Database initialized.")

@cli.command("seed")
def seed():
    """Seed the database with sample data."""
    seed_data()
    click.echo("Seed data added.")

# -----------------------------
# User Commands
# -----------------------------
@cli.command("create-user")
@click.argument("username")
def create_user(username):
    """Create a new user."""
    session = get_session()
    if session.query(User).filter_by(username=username).first():
        click.echo(f"User '{username}' already exists.")
        return
    user = User(username=username)
    session.add(user)
    session.commit()
    click.echo(f"User '{username}' created.")

@cli.command("list-users")
def list_users():
    """List all users."""
    session = get_session()
    users = session.query(User).all()
    if not users:
        click.echo("No users found.")
        return
    click.echo("Users:")
    for user in users:
        click.echo(f"- {user.username}")

@cli.command("delete-user")
@click.argument("username")
def delete_user(username):
    """Delete a user and all their tasks."""
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        click.echo(f"User '{username}' not found.")
        return
    session.delete(user)
    session.commit()
    click.echo(f"User '{username}' deleted.")

# -----------------------------
# Task Commands
# -----------------------------
@cli.command("add-task")
@click.argument("username")
@click.argument("title")
@click.option("-d", "--description", default="", help="Task description")
@click.option("-p", "--priority", default=1, type=int, help="Task priority")
def add_task(username, title, description, priority):
    """Add a task for a user."""
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        click.echo(f"User '{username}' does not exist.")
        return
    task = Task(title=title, description=description, priority=priority, owner=user)
    session.add(task)
    session.commit()
    click.echo(f"Task '{title}' added for {username}.")

@cli.command("list-tasks")
@click.argument("username")
def list_tasks(username):
    """List all tasks for a user."""
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        click.echo(f"User '{username}' does not exist.")
        return
    tasks = session.query(Task).filter_by(owner=user).all()
    if not tasks:
        click.echo(f"No tasks for {username}.")
        return
    for t in tasks:
        status = "[x]" if t.completed else "[ ]"
        click.echo(f"{status} {t.id}: {t.title} (priority={t.priority})")

@cli.command("complete-task")
@click.argument("task_id", type=int)
def complete_task(task_id):
    """Mark a task as complete by task ID."""
    session = get_session()
    task = session.query(Task).get(task_id)
    if not task:
        click.echo(f"Task with ID {task_id} does not exist.")
        return
    task.completed = True
    session.commit()
    click.echo(f"Task {task_id} completed.")

# -----------------------------
# Run CLI
# -----------------------------
if __name__ == "__main__":
    cli()
