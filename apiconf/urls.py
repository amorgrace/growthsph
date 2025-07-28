from django.urls import path
from .views import WalletAddressView, UserFinancesView, UserTransactionListView, KYCUploadView
from .views import test_email_view
from apiconf.views import ActivateUserView

urlpatterns = [
    path('wallet/', WalletAddressView.as_view(), name='wallet-address'),
    path('user/finance/', UserFinancesView.as_view(), name='user-finance'),
    path('user/transactions/', UserTransactionListView.as_view(), name='user-transactions'),
    path('kyc-upload/', KYCUploadView.as_view(), name='kyc'),
    path("test-email/", test_email_view, name="test-email"),
    path("activate/<uid>/<token>/", ActivateUserView.as_view(), name="user-activate"),
] 
