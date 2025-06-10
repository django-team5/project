from django.db import models

# 계좌 모델
class Account(models.Model):
    name = models.CharField(max_length=100)  # 계좌명
    balance = models.IntegerField(default=0) # 잔액

# 거래내역 모델
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # 계좌 참조
    amount = models.IntegerField()  # 거래 금액
    description = models.CharField(max_length=255)  # 설명
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일 

