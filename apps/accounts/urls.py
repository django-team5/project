from django.urls import path
from .views import SignupView, LoginView, AccountListCreateView

# accounts 앱의 URL 패턴
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  # 회원가입
    path('login/', LoginView.as_view(), name='login'),    # 로그인
    path('', AccountListCreateView.as_view(), name='account-list-create'),  # 계좌 목록/생성
] 