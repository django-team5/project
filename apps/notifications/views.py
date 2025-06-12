from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from .serializers import NotificationSerializer

class NotificationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# 알림 목록 조회 및 생성 API
class NotificationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotificationPagination

    def get(self, request):
        # 본인 알림만 조회
        notifications = Notification.objects.filter(user=request.user)
        
        # 페이지네이션 적용
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(notifications, request)
        
        if page is not None:
            serializer = NotificationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # 알림 생성
        serializer = NotificationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 알림 상세 조회, 수정, 삭제 API
class NotificationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Notification.objects.get(pk=pk, user=user)
        except Notification.DoesNotExist:
            return None

    def get(self, request, pk):
        notification = self.get_object(pk, request.user)
        if not notification:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def patch(self, request, pk):
        notification = self.get_object(pk, request.user)
        if not notification:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        notification = self.get_object(pk, request.user)
        if not notification:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 일괄 읽음 처리 API
class NotificationBulkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # 사용자의 모든 읽지 않은 알림을 읽음 처리
        updated_count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).update(is_read=True)
        
        return Response({
            'message': f'{updated_count}개의 알림을 읽음 처리했습니다.',
            'updated_count': updated_count
        }, status=status.HTTP_200_OK) 