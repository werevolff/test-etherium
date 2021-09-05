from django.conf import settings
from web3 import Web3


def get_w3() -> Web3:
    """Returns Web3 connection Client."""
    provider = Web3.HTTPProvider(settings.W3_PROVIDER_URL)
    return Web3(provider)
