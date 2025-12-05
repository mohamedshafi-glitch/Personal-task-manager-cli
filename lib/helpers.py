from .models.base import SessionLocal

def get_session():
    """Return a new database session."""
    return SessionLocal()
