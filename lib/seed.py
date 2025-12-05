from lib.helpers import get_session, Base, engine
from lib.models.user import User
from lib.models.task import Task

def seed_data():
    Base.metadata.create_all(engine)
    session = get_session()
    try:
        if session.query(User).first():
            return
        alice = User(username="alice")
        bob = User(username="bob")
        session.add_all([alice, bob])
        session.commit()

        t1 = Task(title="Buy groceries", description="Milk, eggs", owner=alice, priority=2)
        t2 = Task(title="Read ORM chapter", owner=alice, priority=3)
        t3 = Task(title="Pay rent", owner=bob, priority=1)

        session.add_all([t1, t2, t3])
        session.commit()
    finally:
        session.close()
