from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Account
from .serializers import AccountSerializer

User = get_user_model()

class AccountModelTest(TestCase):
    """Account 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_account_creation(self):
        """계좌 생성 테스트"""
        account = Account.objects.create(
            owner=self.user,
            name='테스트 계좌',
            account_number='1234567890',
            bank_code='004',
            account_type='CHECKING',
            balance=10000
        )
        self.assertEqual(account.owner, self.user)
        self.assertEqual(account.name, '테스트 계좌')
        self.assertEqual(account.balance, 10000)
        self.assertTrue(account.created_at)
    
    def test_account_str_method(self):
        """계좌 __str__ 메서드 테스트"""
        account = Account.objects.create(
            owner=self.user,
            name='테스트 계좌',
            account_number='1234567890',
            bank_code='004',
            account_type='CHECKING',
            balance=10000
        )
        expected = '테스트 계좌 (1234567890, 10000원)'
        self.assertEqual(str(account), expected)
    
    def test_account_number_unique(self):
        """계좌번호 중복 방지 테스트"""
        Account.objects.create(
            owner=self.user,
            name='계좌1',
            account_number='1234567890',
            bank_code='004',
            account_type='CHECKING'
        )
        with self.assertRaises(Exception):
            Account.objects.create(
                owner=self.user,
                name='계좌2',
                account_number='1234567890',  # 중복 계좌번호
                bank_code='004',
                account_type='CHECKING'
            )

class AccountSerializerTest(TestCase):
    """Account 시리얼라이저 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            owner=self.user,
            name='테스트 계좌',
            account_number='1234567890',
            bank_code='004',
            account_type='CHECKING',
            balance=10000
        )
    
    def test_serializer_data(self):
        """시리얼라이저 데이터 검증"""
        serializer = AccountSerializer(self.account)
        data = serializer.data
        self.assertEqual(data['owner'], self.user.email)
        self.assertEqual(data['name'], '테스트 계좌')
        self.assertEqual(data['account_number'], '1234567890')
        self.assertEqual(data['balance'], 10000)

class AccountAPITest(APITestCase):
    """Account API 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.account = Account.objects.create(
            owner=self.user,
            name='테스트 계좌',
            account_number='1234567890',
            bank_code='004',
            account_type='CHECKING',
            balance=10000
        )
        self.url = reverse('account-list-create')
    
    def test_get_accounts_authenticated(self):
        """인증된 사용자의 계좌 조회 테스트"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], '테스트 계좌')
    
    def test_get_accounts_unauthenticated(self):
        """비인증 사용자의 계좌 조회 테스트"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_account(self):
        """계좌 생성 테스트"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': '새 계좌',
            'account_number': '9876543210',
            'bank_code': '088',
            'account_type': 'SAVING',
            'balance': 5000
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)
        new_account = Account.objects.get(account_number='9876543210')
        self.assertEqual(new_account.owner, self.user)
    
    def test_user_can_only_see_own_accounts(self):
        """사용자는 본인 계좌만 조회 가능 테스트"""
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        Account.objects.create(
            owner=other_user,
            name='다른 사용자 계좌',
            account_number='5555555555',
            bank_code='004',
            account_type='CHECKING'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # 본인 계좌만 조회
        self.assertEqual(response.data[0]['account_number'], '1234567890') 