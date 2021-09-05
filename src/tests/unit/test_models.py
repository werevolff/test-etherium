import pytest


def test_wallet_secret_field_uses_encryptor(
    mock_fernet_encrypt,
    mock_fernet_decrypt,
    wallet,
):
    wallet.refresh_from_db()
    mock_fernet_encrypt.assert_called_once()
    mock_fernet_decrypt.assert_called_once()


@pytest.mark.parametrize(
    'create_kwargs,expected_mock_called',
    (
        ({'address': 'address', 'private_key': 'private_key'}, False),
        ({'address': 'address'}, False),
        ({'private_key': 'private_key'}, True),
        ({}, True),
    ),
)
def test_wallet_creation(
    wallet_factory,
    mock_wallet_create_new_address,
    create_kwargs,
    expected_mock_called,
):
    wallet_factory(**create_kwargs)
    if expected_mock_called:
        mock_wallet_create_new_address.assert_called_once()
    else:
        mock_wallet_create_new_address.assert_not_called()
