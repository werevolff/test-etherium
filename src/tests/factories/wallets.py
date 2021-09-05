import secrets

import factory
from factory.django import DjangoModelFactory

from applications.wallets.models import Wallet


class WalletFactory(DjangoModelFactory):
    """Factory for Wallet model."""
    currency = Wallet.DEFAULT_WALLET_CURRENCY

    @factory.lazy_attribute
    def private_key(self):
        """Generates private key."""
        return '0x' + secrets.token_hex(32)

    @factory.lazy_attribute
    def address(self):
        """Generates address."""
        return secrets.token_hex(21)

    class Meta:
        model = Wallet
        django_get_or_create = ('address', 'currency')
