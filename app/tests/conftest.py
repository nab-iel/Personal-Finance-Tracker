import pytest
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.models import User

@pytest.fixture(scope="function")
def session():
    if not engine.url.get_backend_name() == "sqlite":
        raise RuntimeError('Use SQLite backend to run tests')

    Base.metadata.create_all(engine)
    try:
        with Session() as session:
            yield session
    finally:
        Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def seed(session):
    session.add_all(
        [
            User(id=1, username="example1", email="example1@gmail.com", password="123"),
            User(id=2, username="example2", email="example2@gmail.com", password="456"),
        ]
    )
    session.commit()