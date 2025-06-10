from rest_framework import serializers
from .models import Account

# 계좌(Account) 시리얼라이저
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'account_number', 'balance', 'created_at']

# 예시용 Serializer (추후 구현) 

# accounts 앱의 시리얼라이저 정의 (예시) 