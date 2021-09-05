import pytest


@pytest.mark.usefixtures('mock_fernet_decrypt')
def test_wallet_private_key_decrypted(wallet, decrypted_wallet_private_key):
    wallet.refresh_from_db()
    assert wallet.private_key == decrypted_wallet_private_key
