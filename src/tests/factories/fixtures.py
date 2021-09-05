import secrets
from unittest.mock import Mock

import pytest

from tests.factories.wallets import WalletFactory


@pytest.fixture
def wallet(wallet_factory):
    return wallet_factory()


@pytest.fixture
def wallet_factory():
    return WalletFactory


@pytest.fixture
def mock_fernet_encrypt(mocker, encrypted_wallet_private_key) -> Mock:
    return mocker.patch(
        'applications.wallets.encryptors.WalletSecretFernetEncryptor.encrypt',
        return_value=encrypted_wallet_private_key,
    )


@pytest.fixture
def mock_fernet_decrypt(mocker, decrypted_wallet_private_key) -> Mock:
    return mocker.patch(
        'applications.wallets.encryptors.WalletSecretFernetEncryptor.decrypt',
        return_value=decrypted_wallet_private_key,
    )


@pytest.fixture
def encrypted_wallet_private_key() -> str:
    return 'encrypted-private-key'


@pytest.fixture
def decrypted_wallet_private_key() -> str:
    return 'decrypted-private-key'


@pytest.fixture(autouse=True)
def mock_wallet_query_set_create_new_address(mocker) -> Mock:
    return mocker.patch(
        'applications.wallets.querysets.WalletQuerySet._create_new_address',
        return_value='0x' + secrets.token_hex(20),
    )
