from django.db import models

# 기본 User 모델을 사용합니다. (확장 필요시 커스텀 가능)

# Create your models here. 

# accounts 앱의 모델 정의 (예시) 

# 계좌(Account) 모델 예시
class Account(models.Model):
    name = models.CharField(max_length=100)  # 계좌명
    balance = models.IntegerField(default=0) # 잔액
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일

    def __str__(self):
        return f"{self.name} ({self.balance}원)" 