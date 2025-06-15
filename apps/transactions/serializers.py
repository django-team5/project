from rest_framework import serializers
from .models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(
        source='account.account_number',
        read_only=True,
        help_text='계좌번호'
    )

    account = serializers.PrimaryKeyRelatedField(
        queryset=TransactionHistory._meta.get_field('account').remote_field.model.objects.all(),
        help_text='거래를 적용할 계좌의 ID (PK)'
    )

    amount = serializers.IntegerField(help_text='거래 금액 (양수)')
    description = serializers.CharField(help_text='거래 내용', required=False, allow_blank=True)
    inout_type = serializers.ChoiceField(
        choices=[('입금', '입금'), ('출금', '출금')],
        help_text="입출금 구분: '입금' 또는 '출금'"
    )
    transaction_method = serializers.ChoiceField(
        choices=[('계좌이체', '계좌이체'), ('현금', '현금'), ('카드', '카드')],
        help_text="거래 수단: '계좌이체', '현금', '카드'"
    )
    transaction_datetime = serializers.DateTimeField(help_text='거래 발생 시각 (ISO 8601 형식)', required=True)

    class Meta:
        model = TransactionHistory
        fields = [
            'id',
            'account',
            'account_number',
            'amount',
            'balance_after',
            'description',
            'inout_type',
            'transaction_method',
            'transaction_datetime',
            'created_at',
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
                raise serializers.ValidationError("잔액이 부족합니다")
            account.balance -= amount
        else:
            raise serializers.ValidationError("유효하지 않은 유형입니다")

        # 계좌 잔액 저장
        account.save()

        # 거래 후 잔액 기록
        validated_data['balance_after'] = account.balance

        # 거래 내역 저장
        return super().create(validated_data)
