from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.wallets.models import Wallet
from applications.wallets.serializers import (
    WalletSerializer,
    WalletTransferSerializer,
)


class WalletViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """ViewSet for Wallets."""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @action(
        methods=('post',),
        detail=False,
        serializer_class=WalletTransferSerializer,
    )
    def transfer(self, request, *args, **kwargs) -> Response:
        """Transfer Ethereum from one wallet to another."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
