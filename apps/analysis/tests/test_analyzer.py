import tempfile
from datetime import datetime, timedelta
from decimal import Decimal
from django.test import TestCase
import pytest
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model

from apps.accounts.models import Account
from apps.transactions.models import TransactionHistory
from apps.analysis.models import Analysis
from apps.analysis.logic import Analyzer

User = get_user_model()

@pytest.mark.django_db
def test_analyzer_creates_analysis_and_image():
    #사용자 및 계좌 생성
    user = User.objects.create_user(email='test@example.com', password='pass1234')
    account = Account.objects.create(
        owner=user,
        name='테스트 계좌',
        account_number='1234567890',
        bank_code='004',
        account_type='입출금',
        balance=1000000
    )

    #거래내역 생성 (일주일)
    today = datetime.now()
    for i in range(7):
        TransactionHistory.objects.create(
            account=account,
            amount=Decimal('10000.00'),
            balance_after=Decimal('1000000.00') - i * Decimal('10000.00'),
            description='테스트 지출',
            inout_type='출금',
            transaction_method='카드결제',
            transaction_datetime=today - timedelta(days=i)
        )

    #분석기 실행
    analyzer = Analyzer(
        user=user,
        target_type='출금',
        period_type='일간',
        start_date=(today - timedelta(days=7)).date(),
        end_date=today.date()
    )
    analysis = analyzer.run()

    #검증
    assert isinstance(analysis, Analysis)
    assert analysis.user == user
    assert analysis.target_type == '출금'
    assert analysis.period_type == '일간'
    assert analysis.result_image_url.name.endswith('.png')
    assert default_storage.exists(analysis.result_image_url.name)

class AnalyzerTestCase(TestCase):
    def test_analyzer_creates_analysis(self):
        user = User.objects.create_user(email='test@example.com', password='pass1234')
        account = Account.objects.create(
            owner=user,
            name='테스트 계좌',
            account_number='1234567890',
            bank_code='004',
            account_type='입출금',
            balance=1000000
        )

        today = datetime.now()
        for i in range(5):
            TransactionHistory.objects.create(
                account=account,
                amount=Decimal('10000.00'),
                balance_after=Decimal('1000000.00') - i * Decimal('10000.00'),
                description='테스트 지출',
                inout_type='출금',
                transaction_method='카드결제',
                transaction_datetime=today - timedelta(days=i)
            )

        analyzer = Analyzer(
            user=user,
            target_type='출금',
            period_type='일간',
            start_date=(today - timedelta(days=5)).date(),
            end_date=today.date()
        )
        analysis = analyzer.run()

        self.assertEqual(analysis.user, user)
        self.assertEqual(analysis.target_type, '출금')
        self.assertTrue(analysis.result_image_url.name.endswith('.png'))