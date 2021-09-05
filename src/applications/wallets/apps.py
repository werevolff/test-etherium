from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WalletsConfig(AppConfig):
    """Custom configuration for wallets app."""
    name = 'applications.wallets'
    verbose_name = _('wallets')
