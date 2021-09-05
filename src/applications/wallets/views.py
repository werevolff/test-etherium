from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from applications.wallets.models import Wallet
from applications.wallets.serializers import WalletSerializer


class WalletViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """ViewSet for Wallets."""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
