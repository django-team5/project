from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PingView(APIView):
    @swagger_auto_schema(
        operation_summary="테스트",
        operation_description="서버 응답 확인 테스트 api",
        responses={200: openapi.Response(description="성공")},
    )
    def get(self, request):
        return Response({"message": "서버 응답"}, status=status.HTTP_200_OK)
