from django.db import models
from django.conf import settings
from .constants import BANK_CODES, ACCOUNT_TYPE

# 계좌(Account) 모델
class Account(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')  # 소유자
    name = models.CharField(max_length=100)  # 계좌명
    account_number = models.CharField(max_length=20, unique=True)  # 계좌번호
    bank_code = models.CharField(max_length=10, choices=BANK_CODES)  # 은행 코드
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)  # 계좌 종류
    balance = models.IntegerField(default=0)  # 잔액
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일

    def __str__(self):
        return f"{self.name} ({self.account_number}, {self.balance}원)" 