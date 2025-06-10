from django.db import models

# 계좌(Account) 모델 예시
class Account(models.Model):
    name = models.CharField(max_length=100)  # 계좌명
    account_number = models.CharField(max_length=20, unique=True)  # 계좌번호 (중복 불가)
    balance = models.IntegerField(default=0) # 잔액
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일

    def __str__(self):
        return f"{self.name} ({self.account_number}, {self.balance}원)" 