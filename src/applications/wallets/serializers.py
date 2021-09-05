from rest_framework import serializers

from applications.wallets.models import Wallet


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
