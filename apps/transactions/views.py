from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.accounts.models import Account
from apps.accounts.serializers import AccountSerializer
from .models import TransactionHistory
from .serializers import TransactionHistorySerializer
from .constants import TRANSACTION_TYPE, TRANSACTION_METHOD

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
        # 필터링
        account = request.query_params.get('account')
        type = request.query_params.get('type')
        category = request.query_params.get('category')
        period = request.query_params.get('period')
        
        # 기본 쿼리셋
        transactions = TransactionHistory.objects.filter(account__owner=request.user)
        
        # 필터 적용
        if account:
            transactions = transactions.filter(account_id=account)
        if type:
            transactions = transactions.filter(inout_type='입금' if type == 'income' else '출금')
        if category:
            transactions = transactions.filter(transaction_method=category)
        if period:
            from datetime import datetime, timedelta
            now = datetime.now()
            if period == 'today':
                transactions = transactions.filter(transaction_datetime__date=now.date())
            elif period == 'week':
                start_date = now - timedelta(days=now.weekday())
                transactions = transactions.filter(transaction_datetime__date__gte=start_date.date())
            elif period == 'month':
                transactions = transactions.filter(transaction_datetime__month=now.month)
            elif period == 'year':
                transactions = transactions.filter(transaction_datetime__year=now.year)
        
        # 정렬
        transactions = transactions.order_by('-transaction_datetime')
        
        # 페이지네이션
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        # 데이터 직렬화
        serializer = TransactionHistorySerializer(transactions[start:end], many=True)
        
        # 응답 데이터 구성
        return Response({
            'results': serializer.data,
            'count': transactions.count()
        })

    def post(self, request):
        serializer = TransactionHistorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            account = serializer.validated_data['account']
            if account.owner != request.user:
                return Response({"detail": "본인의 계좌만 사용할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 카테고리 목록
class CategoryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 거래 유형과 거래 수단을 카테고리로 사용
        categories = [
            {"id": "type_" + code, "name": name} for code, name in TRANSACTION_TYPE
        ] + [
            {"id": "method_" + code, "name": name} for code, name in TRANSACTION_METHOD
        ]
        return Response(categories)

