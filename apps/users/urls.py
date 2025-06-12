from django.urls import path
from .views import SignupView, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]

