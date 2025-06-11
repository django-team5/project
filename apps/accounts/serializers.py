from rest_framework import serializers
from .models import Account

# 계좌(Account) 시리얼라이저
class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()  # 소유자 이메일

    class Meta:
        model = Account
        fields = ['id', 'owner', 'name', 'account_number', 'bank_code', 'account_type', 'balance', 'created_at']

    def get_owner(self, obj):
        return obj.owner.email  # 소유자 이메일 반환

# 예시용 Serializer (추후 구현) 

# accounts 앱의 시리얼라이저 정의 (예시) 