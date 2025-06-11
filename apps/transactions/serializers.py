from rest_framework import serializers
from .models import TransactionHistory

class TransactionHistorySerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(source='account.account_number', read_only=True)

    class Meta:
        model = TransactionHistory
        fields = [
            'id',
            'account',              # 계좌 PK 입력
            'account_number',       # 계좌번호 출력
            'amount',               # 거래 금액
            'balance_after',        # 거래 후 잔액
            'description',          # 거래 설명
            'inout_type',           # 입출금 유형
            'transaction_method',   # 거래 수단
            'transaction_datetime', # 거래 발생 시각
            'created_at',           # 저장 시각
        ]
        read_only_fields = ['balance_after', 'created_at']

    def create(self, validated_data):
        account = validated_data['account']
        amount = validated_data['amount']
        inout_type = validated_data['inout_type']

        # 입출금 처리
        if inout_type == '입금':
            account.balance += amount
        elif inout_type == '출금':
            if account.balance < amount:
                raise serializers.ValidationError("잔액이 부족합니다.")
            account.balance -= amount
        else:
            raise serializers.ValidationError("유효하지 않은 입출금 유형입니다.")

        # 계좌 잔액 저장
        account.save()

        # 거래 후 잔액을 기록에 저장
        validated_data['balance_after'] = account.balance

        # 거래 내역 생성
        return super().create(validated_data)
