from django.db import models

# 알림 모델
class Notification(models.Model):
    message = models.CharField(max_length=255)  # 알림 메시지
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    is_read = models.BooleanField(default=False)  # 읽음 여부

# Create your models here. 