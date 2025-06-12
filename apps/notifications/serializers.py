from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """Notification 모델 시리얼라이저"""
    class Meta:
        model = Notification
        fields = ['id', 'message', 'type', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # 현재 사용자를 자동으로 설정
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 