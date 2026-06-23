"""Database engine, session factory, and base class for models."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ensure the data directory exists before SQLite tries to open a file there.
Path("data").mkdir(parents=True, exist_ok=True)

DATABASE_URL = "sqlite:///data/supportgenie.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()