
def test_wallet_secret_field_uses_encryptor(
    mock_fernet_encrypt,
    mock_fernet_decrypt,
    wallet,
):
    wallet.refresh_from_db()
    mock_fernet_encrypt.assert_called_once()
    mock_fernet_decrypt.assert_called_once()
