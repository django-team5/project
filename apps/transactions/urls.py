from django.urls import path
from .views import TransactionCreateView, AccountListCreateView, TransactionListCreateView

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
]

