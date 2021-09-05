import pytest


@pytest.fixture(autouse=True)
def init_database(db):
    """Init database for all tests."""
    return db
