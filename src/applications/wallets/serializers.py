import re
import secrets

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from applications.wallets.models import Wallet


def ethereum_address_validator(value:str):
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

    def validate(self, attrs):
        """Override validation."""
        wallet = Wallet.objects.filter(
            address=attrs.get('_from'),
            currency=attrs.get('currency'),
        ).first()
        if not wallet:
            error_message = _(
                'Wallet {0} with currency {1} does not exists',
            ).format(attrs.get('_from'), attrs.get('currency'))
            raise serializers.ValidationError({'_from': error_message})
        return attrs

    def create(self, validated_data):
        """Create transaction."""
        return {'hash': secrets.token_hex(32), 'nonce': 0}
