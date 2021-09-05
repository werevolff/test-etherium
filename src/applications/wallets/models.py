import importlib
import secrets
from typing import TYPE_CHECKING, Type

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from main.w3 import get_w3

if TYPE_CHECKING:
    from applications.wallets.encryptors import WalletSecretEncryptorInterface


class WalletSecretField(models.CharField):
    """Field to store Wallet.private_key."""

    def get_prep_value(self, value: str):
        """Override get_prep_value."""
        encryptor = self._get_encryptor()
        return encryptor.encrypt(value)

    def from_db_value(self, value: str, *args):
        """Decrypt value from database."""
        encryptor = self._get_encryptor()
        return encryptor.decrypt(value)

    def _get_encryptor(self) -> Type['WalletSecretEncryptorInterface']:
        """Get current encryptor class."""
        parts = settings.WALLET_PRIVATE_KEY_ENCRYPTOR.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)


class Wallet(models.Model):
    """Wallet model."""

    class WalletCurrencyChoices(models.TextChoices):
        """Choices for Wallet.currency field."""

        ETHERIUM = 'eth', 'etherium'

    DEFAULT_WALLET_CURRENCY = WalletCurrencyChoices.ETHERIUM

    private_key = WalletSecretField(
        verbose_name=_('private_key'),
        max_length=250,
    )
    address = models.CharField(
        verbose_name=_('address'),
        max_length=42,
    )
    currency = models.CharField(
        verbose_name=_('currency'),
        max_length=3,
        choices=WalletCurrencyChoices.choices,
        default=DEFAULT_WALLET_CURRENCY,
    )

    def save(self, *args, **kwargs) -> None:
        """Override save() method."""
        if not self.private_key:
            self.private_key = '0x' + secrets.token_hex(32)
        if not self.address:
            self.address = self._create_new_address(self.private_key)
        return super().save(*args, **kwargs)

    def _create_new_address(self) -> str:
        """Create new etherium address"""
        w3 = get_w3()
        account = w3.eth.account.from_key(self.private_key)
        return account.address

    def __str__(self):
        return f'{self.currency} - {self.address}'

    class Meta:
        verbose_name = _('wallet')
        verbose_name_plural = _('wallets')
        ordering = ('-id',)
        unique_together = (
            ('address', 'currency'),
        )
