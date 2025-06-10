from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .logic import simple_analysis

# Create your views here.

# 분석 API 예시
class AnalysisView(APIView):
    def post(self, request):
        # 분석 로직 호출
        result = simple_analysis(request.data)
        return Response(result, status=status.HTTP_200_OK)

# analysis 앱의 뷰 정의 (예시) 