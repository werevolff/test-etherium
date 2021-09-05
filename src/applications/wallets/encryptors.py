from cryptography.fernet import Fernet
from django.conf import settings


class WalletSecretFernetEncryptor(object):
    """Encrypt and decrypt Wallet.private_key with Fernet."""

    @classmethod
    def encrypt(cls, private_key: str) -> str:
        """Encrypt private key."""
        fernet = Fernet(settings.FERNET_KEY)
        return fernet.encrypt(private_key.encode()).decode()

    @classmethod
    def decrypt(cls, value_from_db: str) -> str:
        """Decrypt private_key."""
        fernet = Fernet(settings.FERNET_KEY)
        return fernet.decrypt(value_from_db.encode()).decode()
