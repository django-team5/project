from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# 거래내역 리스트/생성 예시
class TransactionListCreateView(APIView):
    def get(self, request):
        # 거래내역 조회 로직 작성
        return Response({'message': '거래내역 리스트'}, status=status.HTTP_200_OK)

    def post(self, request):
        # 거래내역 생성 로직 작성
        return Response({'message': '거래내역 생성'}, status=status.HTTP_201_CREATED) 

