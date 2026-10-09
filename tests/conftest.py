# Why: each database integration test has a clean schema and no shared rows.
import pytest
from app.providers.database.models import Base
from app.providers.database.session import get_engine

@pytest.fixture(autouse=True)
def reset_database():
    engine=get_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
