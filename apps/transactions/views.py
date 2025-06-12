from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.accounts.models import Account
from apps.accounts.serializers import AccountSerializer
from .models import TransactionHistory
from .serializers import TransactionHistorySerializer

#계좌목록, 조회 생성
class AccountListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(owner=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = AccountSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#입출금 생성
class TransactionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TransactionHistorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            account = serializer.validated_data['account']
            # 소유자 확인
            if account.owner != request.user:
                return Response({"detail": "본인의 계좌만 사용할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 거래조회 + 생성
class TransactionListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = TransactionHistory.objects.filter(account__owner=request.user).order_by('-transaction_datetime')
        serializer = TransactionHistorySerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionHistorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            account = serializer.validated_data['account']
            if account.owner != request.user:
                return Response({"detail": "본인의 계좌만 사용할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

