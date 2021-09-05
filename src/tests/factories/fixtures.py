import pytest

from tests.factories.wallets import WalletFactory


@pytest.fixture
def wallet():
    return WalletFactory()
