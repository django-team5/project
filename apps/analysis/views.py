from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import AnalysisSerializer
from .logic import Analyzer


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
