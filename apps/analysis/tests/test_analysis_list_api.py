from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.analysis.models import Analysis
from datetime import date

User = get_user_model()

class AnalysisListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass')
        self.client.login(email='test@example.com', password='testpass')

        # 월간 분석 데이터 2개
        Analysis.objects.create(
            user=self.user,
            target_type='출금',
            period_type='월간',
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            summary='1월 분석 결과'
        )
        Analysis.objects.create(
            user=self.user,
            target_type='출금',
            period_type='월간',
            start_date=date(2024, 2, 1),
            end_date=date(2024, 2, 28),
            summary='2월 분석 결과'
        )

        # 주간 분석 데이터 1개
        Analysis.objects.create(
            user=self.user,
            target_type='수입',
            period_type='주간',
            start_date=date(2024, 3, 1),
            end_date=date(2024, 3, 7),
            summary='3월 분석 결과'
        )

    def test_list_all_analyses(self):
        url = reverse('analysis-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_period_type(self):
        url = reverse('analysis-list')
        response = self.client.get(url, {'period_type': '월간'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for item in response.data:
            self.assertEqual(item['period_type'], '월간')
