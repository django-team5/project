from django.urls import path
from .views import NotificationListView, NotificationDetailView, NotificationBulkReadView

# 알림 URL 패턴
urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),  # 알림 전체 조회/생성
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),  # 단일 알림 조회/삭제/읽음
    path('read/all/', NotificationBulkReadView.as_view(), name='notification-bulk-read'),  # 알림 일괄 읽음 처리
] 