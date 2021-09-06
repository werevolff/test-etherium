import re
from typing import Any, Dict

from django.conf import settings
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

    @property
    def actual_nonce(self) -> int:
        """Get number of transaction."""
        return self.w3.eth.get_transaction_count(self.wallet.address)

    @cached_property
    def w3(self) -> Web3:
        """Web3py instance."""
        return get_w3()

    def validate(self, attrs: Dict[str, Any]):
        """Override validation."""
        self._validate_wallet_exists(attrs)
        self._validate_balance()
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create transaction."""
        transaction_hex = self._send_transaction(validated_data['_to'])
        return {'hash': transaction_hex, 'nonce': self.actual_nonce}

    def _send_transaction(self, recipient_address: str) -> str:
        """Send transaction to recipient wallet."""
        defaults = settings.ETHEREUM_TRANSACTIONS_DEFAULTS
        gas_price_as_gwei = Web3.fromWei(self.gas_price, 'gwei')
        sign_params = {
            'nonce': self.actual_nonce,
            'maxFeePerGas': defaults['maxFeePerGas'],
            'maxPriorityFeePerGas': defaults['maxPriorityFeePerGas'],
            'gas': int(gas_price_as_gwei),
            'to': recipient_address,
            'value': self.balance,
            'data': b'',
            'type': defaults['type'],
            'chanId': defaults['chanId'],
        }
        signed_txn = self.w3.eth.account.sign_transaction(
            sign_params,
            self.wallet.private_key,
        )
        hex_bytes = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return hex_bytes.hex()

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
        wallet = Wallet.objects.filter(
            address=attrs.get('_from'),
            currency=attrs.get('currency'),
        ).first()
        if not wallet:
            error_message = _(
                'Wallet {0} with currency {1} does not exists',
            ).format(attrs.get('_from'), attrs.get('currency'))
            raise serializers.ValidationError({'_from': error_message})
        self.wallet = wallet
