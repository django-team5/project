from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Account
from .serializers import AccountSerializer

# 계좌 목록 조회 및 생성 API
class AccountListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근

    def get(self, request):
        # 본인 계좌만 조회
        accounts = Account.objects.filter(owner=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # 계좌 생성 (owner는 현재 로그인 사용자)
        data = request.data.copy()
        data['owner'] = request.user.id  # owner 필드에 현재 사용자 id 할당
        serializer = AccountSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 