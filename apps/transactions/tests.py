from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime

from apps.users.models import User
from apps.accounts.models import Account
from apps.transactions.models import TransactionHistory


class TransactionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            nickname='testnick',
            name='테스트유저'
        )
        self.client.force_authenticate(user=self.user)

        self.account = Account.objects.create(
            owner=self.user,
            name='내 통장',
            balance=100000,
            account_number='000111222'
        )

        self.url = reverse('transaction-list-create')

    def test_create(self): #입출금 생성
        data = {
            "account": self.account.id,
            "amount": "5000.00",
            "balance_after": "105000.00",
            "description": "입금 테스트",
            "inout_type": "입금",
            "transaction_method": "현금",
            "transaction_datetime": datetime.now().isoformat()
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        transactions = TransactionHistory.objects.all()
        self.assertEqual(transactions.count(), 1)
        self.assertEqual(transactions[0].amount, 5000)

    def test_get(self): #입출금 조회
        TransactionHistory.objects.create(
            account=self.account,
            amount=3000,
            balance_after=97000,
            description="출금 테스트",
            inout_type="출금",
            transaction_method="계좌이체",
            transaction_datetime=datetime.now()
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
