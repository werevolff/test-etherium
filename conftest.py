import pytest

pytest_plugins = (
    'tests.factories.fixtures',
)


@pytest.fixture(autouse=True)
def init_database(db):
    """Init database for all tests."""
    return db
