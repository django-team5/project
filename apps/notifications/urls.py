from django.urls import path
from .views import NotificationListView

# 알림 URL 패턴
urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
] 