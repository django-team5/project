from django.db import models
from django.conf import settings

# 알림 모델
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')  # 알림 대상 사용자
    message = models.CharField(max_length=255)  # 메시지
    type = models.CharField(max_length=50, default='general')  # 알림 종류
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    is_read = models.BooleanField(default=False)  # 읽음 여부

    def __str__(self):
        return f"[{self.user}] {self.message}"

