from django.db import models
from django.utils.translation import ugettext_lazy as _


class Wallet(models.Model):
    """Wallet model."""

    class WalletCurrencyChoices(models.TextChoices):
        """Choices for Wallet.currency field."""

        ETHERIUM = 'eth', 'etherium'

    DEFAULT_WALLET_CURRENCY = WalletCurrencyChoices.ETHERIUM

    private_key = models.CharField(
        verbose_name=_('private_key'),
        max_length=184,
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

    def __str__(self):
        return f'{self.currency} - {self.address}'

    class Meta:
        verbose_name = _('wallet')
        verbose_name_plural = _('wallets')
        ordering = ('-id',)
        unique_together = (
            ('address', 'currency'),
        )
