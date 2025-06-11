from django.db import models
from apps.accounts.models import Account


INOUT_TYPE_CHOICES = [
    ('입금', '입금'),
    ('출금', '출금'),
]

TRANSACTION_METHOD_CHOICES = [
    ('현금', '현금'),
    ('계좌이체', '계좌이체'),
    ('자동이체', '자동이체'),
    ('카드결제', '카드결제'),
]

class TransactionHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255)
    inout_type = models.CharField(max_length=10, choices=INOUT_TYPE_CHOICES)
    transaction_method = models.CharField(max_length=20, choices=TRANSACTION_METHOD_CHOICES)
    transaction_datetime = models.DateTimeField() #실제 거래 시간
    created_at = models.DateTimeField(auto_now_add=True) #시스템에 저장된 거래 시간

    def __str__(self):
        return f"{self.account.account_number} - {self.inout_type} {self.amount}원"
