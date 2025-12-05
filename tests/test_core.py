from lib.helpers import get_session, Base, engine
from lib.models.user import User
from lib.models.task import Task

def test_user_and_task():
    Base.metadata.create_all(engine)
    session = get_session()
    try:
        u = User(username="testuser")
        session.add(u)
        session.commit()

        t = Task(title="Test task", owner=u)
        session.add(t)
        session.commit()

        assert session.query(User).count() > 0
        assert session.query(Task).count() > 0
    finally:
        session.close()
