from django.urls import path
from .views import TransactionListCreateView

# 거래내역 URL 패턴
urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list-create'),
]

# transactions 앱의 URLConf (예시)
urlpatterns = [] 