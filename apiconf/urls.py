from django.urls import path
from .views import WalletAddressView, UserFinancesView, UserTransactionListView, KYCUploadView, ChangePasswordView, UserWalletListCreateView, BankAccountView, ActivateUserView


urlpatterns = [
    path('wallet/', WalletAddressView.as_view(), name='wallet-address'),
    path('user/finance/', UserFinancesView.as_view(), name='user-finance'),
    path('user/transactions/', UserTransactionListView.as_view(), name='user-transactions'),
    # path('kyc-upload/', KYCUploadView.as_view(), name='kyc'),
    path("activate/<uid>/<token>/", ActivateUserView.as_view(), name="user-activate"),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('user/wallet/', UserWalletListCreateView.as_view(), name='wallets'),
    path('user/account/', BankAccountView.as_view(), name='bank-account'),

] 

