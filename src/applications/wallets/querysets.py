import secrets

from django.db.models import QuerySet

from main.w3 import get_w3


class WalletQuerySet(QuerySet):
    """Custom QuerySet for the Wallet model."""

    def create(self, *args, **kwargs):
        """Override method create."""
        if not kwargs.get('private_key'):
            kwargs['private_key'] = '0x' + secrets.token_hex(32)
        if not kwargs.get('address'):
            kwargs['address'] = self._create_new_address(kwargs['private_key'])
        return super().create(*args, **kwargs)

    def _create_new_address(self, private_key: str) -> str:
        """Create new etherium address"""
        w3 = get_w3()
        account = w3.eth.account.from_key(private_key)
        return account.address
