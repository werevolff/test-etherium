from factory.django import DjangoModelFactory

from applications.wallets.models import Wallet


class WalletFactory(DjangoModelFactory):
    """Factory for Wallet model."""
    currency = Wallet.DEFAULT_WALLET_CURRENCY
    address = None

    class Meta:
        model = Wallet
        django_get_or_create = ('address', 'currency')
