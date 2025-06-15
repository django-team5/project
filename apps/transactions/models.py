from django.db import models
from apps.accounts.models import Account
from .constants import TRANSACTION_TYPE, TRANSACTION_METHOD


class TransactionHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255)
    inout_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    transaction_method = models.CharField(max_length=20, choices=TRANSACTION_METHOD)
    transaction_datetime = models.DateTimeField() #실제 거래 시간
    created_at = models.DateTimeField(auto_now_add=True) #시스템에 저장된 거래 시간

    def __str__(self):
        return f"{self.account.account_number} - {self.inout_type} {self.amount}원"
