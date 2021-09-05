import secrets

from applications.wallets.encryptors import WalletSecretFernetEncryptor


def test_wallet_secret_fernet_encryptor():
    """Test WalletSecretFernetEncryptor."""
    private_key = '0x' + secrets.token_hex(32)
    encrypted = WalletSecretFernetEncryptor.encrypt(private_key)
    assert private_key != encrypted
    expected_encrypted_length = 184
    assert len(encrypted) == expected_encrypted_length
    decrypted = WalletSecretFernetEncryptor.decrypt(encrypted)
    assert decrypted == private_key
