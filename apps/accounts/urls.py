from django.urls import path
from .views import AccountListCreateView

# accounts 앱의 URLConf
urlpatterns = [
    path('', AccountListCreateView.as_view(), name='account-list-create'),  # 계좌 목록/생성
] 