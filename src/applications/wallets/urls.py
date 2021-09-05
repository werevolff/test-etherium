from rest_framework.routers import DefaultRouter

from applications.wallets.views import WalletViewSet

app_name = 'wallets'

router = DefaultRouter()
router.register(r'', WalletViewSet, basename='wallets')

urlpatterns = router.urls
