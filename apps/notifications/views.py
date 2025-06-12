from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(APIView):
    """알림 리스트 조회 및 생성 API"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        unread = request.query_params.get('unread')
        if unread == 'true':
            notifications = notifications.filter(is_read=False)
        notif_type = request.query_params.get('type')
        if notif_type:
            notifications = notifications.filter(type=notif_type)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationDetailView(APIView):
    """단일 알림 조회, 삭제, 읽음 처리 API"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NotificationBulkReadView(APIView):
    """알림 일괄 읽음 처리 API"""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        count = notifications.update(is_read=True)
        return Response({'updated': count}, status=status.HTTP_200_OK) 