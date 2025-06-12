from django.db import models
from django.conf import settings

# 알림 타입 선택지
NOTIFICATION_TYPES = [
    ('info', '정보'),
    ('warning', '경고'),
    ('success', '성공'),
    ('error', '오류'),
]

# 알림 모델
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')  # 사용자
    message = models.TextField()  # 알림 메시지
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')  # 알림 타입
    is_read = models.BooleanField(default=False)  # 읽음 여부
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일

    class Meta:
        ordering = ['-created_at']  # 최신순 정렬

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}..."

# Create your models here. 