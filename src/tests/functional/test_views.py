from typing import TYPE_CHECKING, List

import pytest
from factory.fuzzy import FuzzyText
from pytest_drf import (Returns200, Returns201, UsesGetMethod, UsesPostMethod,
                        ViewSetTest)
from pytest_lambda import static_fixture
from rest_framework.reverse import reverse

if TYPE_CHECKING:
    from applications.wallets.models import Wallet


class TestWalletViewSet(ViewSetTest, Returns200, UsesGetMethod):
    """Test WalletViewSet."""

    url = static_fixture(
        reverse('wallets:wallets-list')
    )
    created_wallets = static_fixture(2)

    def test_response(self, json, expected_keys, created_wallets):
        assert len(json) == created_wallets
        for wallet in json:
            returned_keys = list(sorted(wallet.keys()))
            assert expected_keys == returned_keys

    class TestCreateMethod(Returns201, UsesPostMethod):
        """Test creation method."""

        data = static_fixture({})

        def test_response(self, json, expected_keys):
            returned_keys = list(sorted(json.keys()))
            assert expected_keys == returned_keys

    @pytest.fixture
    def expected_keys(self) -> List[str]:
        return list(sorted(['address', 'currency']))

    @pytest.fixture(autouse=True)
    def wallets(self, wallet_factory, created_wallets) -> List['Wallet']:
        return wallet_factory.create_batch(
            created_wallets,
            address=FuzzyText(length=42),
        )
