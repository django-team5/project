from django.urls import path
from .views import NotificationListCreateView, NotificationDetailView, NotificationBulkReadView

# 알림 URL 패턴
urlpatterns = [
    path('', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('bulk-read/', NotificationBulkReadView.as_view(), name='notification-bulk-read'),
] 