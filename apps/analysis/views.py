from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .logic import Analyzer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Analysis
from .serializers import AnalysisSerializer


class AnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        target_type = data.get('target_type')  # '수입' 또는 '지출'
        period_type = data.get('period_type')  # '일간', '월간' 등
        start_date = data.get('start_date')    # '2025-01-01'
        end_date = data.get('end_date')        # '2025-06-01'

        if not all([target_type, period_type, start_date, end_date]):
            return Response({"error": "필수 데이터가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        analyzer = Analyzer(
            user=user,
            target_type=target_type,
            period_type=period_type,
            start_date=start_date,
            end_date=end_date
        )
        analysis = analyzer.run()
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AnalysisListView(ListAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        period_type = self.request.query_params.get('period_type')  # 쿼리 파라미터 사용

        queryset = Analysis.objects.filter(user=user).order_by('-created_at')
        if period_type:
            queryset = queryset.filter(period_type=period_type)
        return queryset