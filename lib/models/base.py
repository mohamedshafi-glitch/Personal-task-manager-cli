from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Engine
engine = create_engine("sqlite:///tasks.db", echo=False)

# Base for models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(bind=engine)
