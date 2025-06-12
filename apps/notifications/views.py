from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# 알림 리스트 API 예시
class NotificationListView(APIView):
    def get(self, request):
        # 알림 리스트 조회 로직 작성
        return Response({'message': '알림 리스트'}, status=status.HTTP_200_OK) 