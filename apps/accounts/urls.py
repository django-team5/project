from django.urls import path
from .views import AccountListCreateView, TransactionCreateView

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('transactions/', TransactionCreateView.as_view(), name='transaction-create'),
]
