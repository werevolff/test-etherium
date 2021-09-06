import re
import secrets
from typing import Any, Dict

from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from web3 import Web3

from applications.wallets.models import Wallet
from main.w3 import get_w3


def ethereum_address_validator(value: str):
    """Check that value is correct Ethereum address."""
    if not re.match(r'^0x[a-fA-F0-9]{40}$', value):
        error_message = _('{0} is incorrect Ethereum address value.').format(
            value,
        )
        raise serializers.ValidationError(error_message)


class WalletSerializer(serializers.ModelSerializer):
    """Serialize Wallets."""

    class Meta:
        model = Wallet
        fields = ('private_key', 'address', 'currency')
        read_only_fields = ('address',)
        extra_kwargs = {
            'private_key': {'write_only': True, 'required': False},
            'currency': {'required': False},
        }


class WalletTransferSerializer(serializers.Serializer):
    """Serialize transfer all ethereum from one wallet to another."""

    _from = serializers.CharField(
        validators=(ethereum_address_validator,),
        write_only=True,
    )
    _to = serializers.CharField(
        validators=(
            ethereum_address_validator,
        ),
        write_only=True,
    )
    currency = serializers.ChoiceField(
        choices=Wallet.WalletCurrencyChoices.choices,
        write_only=True,
    )
    hash = serializers.CharField(read_only=True)
    nonce = serializers.IntegerField(read_only=True)

    wallet: Wallet = Wallet()

    @cached_property
    def balance(self) -> int:
        """Get wallet balance (wei)."""
        return self.w3.eth.get_balance(self.wallet.address)

    @cached_property
    def gas_price(self, ) -> int:
        """Generate gas price (wei)."""
        gas_price = self.w3.eth.generate_gas_price() or 0
        return Web3.toWei(gas_price, 'gwei')

    @cached_property
    def w3(self) -> Web3:
        """Web3py instance."""
        return get_w3()

    def validate(self, attrs: Dict[str, Any]):
        """Override validation."""
        self._set_wallet(attrs)
        self._validate_wallet_exists(attrs)
        self._validate_balance()
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create transaction."""
        return {'hash': secrets.token_hex(32), 'nonce': 0}

    def _validate_balance(self) -> None:
        """Validate balance."""
        if self.balance <= 0:
            error_message = _(
                'Balance of wallet {0} is zero or negative',
            ).format(self.wallet.address)
            raise serializers.ValidationError({'_from': error_message})
        if self.balance <= self.gas_price:
            error_message = _(
                'Balance of wallet {0} does not provide payment of '
                'commission ({1})',
            ).format(self.wallet.address, self.gas_price)
            raise serializers.ValidationError({'_from': error_message})

    def _validate_wallet_exists(self, attrs: Dict[str, Any]) -> None:
        """Validate, that wallet is exists in system."""
        if not self.wallet.id:
            error_message = _(
                'Wallet {0} with currency {1} does not exists',
            ).format(attrs.get('_from'), attrs.get('currency'))
            raise serializers.ValidationError({'_from': error_message})

    def _set_wallet(self, attrs: Dict[str, Any]) -> None:
        """Get wallet instance."""
        wallet = Wallet.objects.filter(
            address=attrs.get('_from'),
            currency=attrs.get('currency'),
        ).first()
        if wallet:
            self.wallet = wallet
