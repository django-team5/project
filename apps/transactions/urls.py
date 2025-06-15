from django.urls import path
from .views import TransactionCreateView, AccountListCreateView, TransactionListCreateView, CategoryListView

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]

