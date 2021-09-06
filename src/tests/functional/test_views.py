import secrets
from copy import deepcopy
from http import HTTPStatus
from typing import TYPE_CHECKING, Dict, List, Optional, TypedDict
from unittest.mock import Mock

import pytest
from factory.fuzzy import FuzzyText
from pytest_drf import UsesGetMethod, UsesPostMethod, ViewSetTest
from pytest_lambda import lambda_fixture, static_fixture
from rest_framework.reverse import reverse

if TYPE_CHECKING:
    from applications.wallets.models import Wallet


class ParamsToTestTransfer(TypedDict):
    """Params to test Wallet's Transfers."""

    data: Dict[str, Optional[str]]
    expected_field_error: str


class TestWalletViewSet(ViewSetTest, UsesPostMethod):
    """Test WalletViewSet."""

    url = static_fixture(
        reverse('wallets:wallets-list')
    )

    class TestTransferAction:
        """Test transfer action."""

        url = static_fixture(
            reverse('wallets:wallets-transfer')
        )
        data = lambda_fixture(
            lambda wallet: {
                '_from': wallet.address,
                '_to': '0x' + secrets.token_hex(20),
                'currency': 'eth',
            },
        )

        def test_response_json(self, response, json):
            assert response.status_code == HTTPStatus.OK
            actual_keys = list(sorted(json.keys()))
            expected_keys = list(sorted(['hash', 'nonce']))
            assert actual_keys == expected_keys

        class TestIncorrectBalance:
            """Test incorrect balance value."""

            def test_response_json(self, response, json):
                assert response.status_code == HTTPStatus.BAD_REQUEST
                assert '_from' in json

            @pytest.fixture(
                autouse=True,
                params=(
                    0,
                    -3,
                    4000000000,
                    3000000000,
                ),
            )
            def mock_get_balance_error(self, mocker, request) -> Mock:
                return mocker.patch(
                    'web3.eth.Eth.get_balance',
                    return_value=request.param,
                )

        class TestTransferBadRequest:
            """Test transfer fields validation."""

            wallet_address = '0x' + secrets.token_hex(20)
            correct_data = {
                '_from': wallet_address,
                '_to': '0x' + secrets.token_hex(20),
                'currency': 'eth',
            }

            def test_fields_validation(self, params, response, json):
                assert response.status_code == HTTPStatus.BAD_REQUEST
                assert params['expected_field_error'] in json

            @pytest.fixture
            def data(self, params) -> Dict[str, str]:
                data = deepcopy(params['data'])
                for key, value in params['data'].items():
                    if not value:
                        del(data[key])
                return data

            @pytest.fixture(params=(
                ParamsToTestTransfer(
                    data={
                        **correct_data,
                        '_from': '0x' + secrets.token_hex(20),
                    },
                    expected_field_error='_from',
                ),
                ParamsToTestTransfer(
                    data={**correct_data, '_from': None},
                    expected_field_error='_from',
                ),
                ParamsToTestTransfer(
                    data={
                        **correct_data,
                        '_from': '1x' + secrets.token_hex(20),
                    },
                    expected_field_error='_from',
                ),
                ParamsToTestTransfer(
                    data={
                        **correct_data,
                        '_from': '0x' + secrets.token_hex(19),
                    },
                    expected_field_error='_from',
                ),
                ParamsToTestTransfer(
                    data={**correct_data, '_to': None},
                    expected_field_error='_to',
                ),
                ParamsToTestTransfer(
                    data={
                        **correct_data,
                        '_to': '1x' + secrets.token_hex(20),
                    },
                    expected_field_error='_to',
                ),
                ParamsToTestTransfer(
                    data={
                        **correct_data,
                        '_to': '0x' + secrets.token_hex(19),
                    },
                    expected_field_error='_to',
                ),
                ParamsToTestTransfer(
                    data={**correct_data, 'currency': None},
                    expected_field_error='currency',
                ),
                ParamsToTestTransfer(
                    data={**correct_data, 'currency': 'unexpected'},
                    expected_field_error='currency',
                ),
            ))
            def params(self, request) -> ParamsToTestTransfer:
                return request.param

            @pytest.fixture(autouse=True)
            def wallet_(self, wallet_factory):
                return wallet_factory(address=self.wallet_address)

    class TestListMethod(UsesGetMethod):
        """Test List Method."""

        created_wallets = static_fixture(2)

        def test_response_json(
            self,
            response,
            json,
            expected_keys,
            created_wallets,
        ):
            assert response.status_code == HTTPStatus.OK
            assert len(json) == created_wallets
            for wallet in json:
                returned_keys = list(sorted(wallet.keys()))
                assert expected_keys == returned_keys

        @pytest.fixture(autouse=True)
        def wallets(self, wallet_factory, created_wallets) -> List['Wallet']:
            return wallet_factory.create_batch(
                created_wallets,
                address=FuzzyText(length=42),
            )

    class TestCreateMethod:
        """Test creation method."""

        data = static_fixture({})

        def test_response_json(self, response, json, expected_keys):
            assert response.status_code == HTTPStatus.CREATED
            returned_keys = list(sorted(json.keys()))
            assert expected_keys == returned_keys


@pytest.fixture
def expected_keys() -> List[str]:
    return list(sorted(['address', 'currency']))


@pytest.fixture(autouse=True)
def mock_get_balance(mocker) -> Mock:
    return mocker.patch(
        'web3.eth.Eth.get_balance',
        return_value=5000000000,
    )


@pytest.fixture(autouse=True)
def mock_generate_gas_price_error(mocker) -> Mock:
    return mocker.patch(
        'web3.eth.Eth.generate_gas_price',
        return_value=4,
    )
