from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """Notification 모델 시리얼라이저"""
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'type', 'created_at', 'is_read']
        read_only_fields = ['user', 'created_at'] 