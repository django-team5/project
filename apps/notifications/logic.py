# notifications/logic.py
# 알림 관련 비즈니스 로직 함수 모음

from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

def create_notification(user, message, notif_type='general'):
    """알림 생성"""
    return Notification.objects.create(user=user, message=message, type=notif_type)

def get_notification_message(event_type, **kwargs):
    """이벤트 타입에 따라 메시지 생성"""
    if event_type == 'comment':
        return f"{kwargs.get('username', '누군가')}님이 댓글을 남겼습니다."
    elif event_type == 'like':
        return f"{kwargs.get('username', '누군가')}님이 좋아요를 눌렀습니다."
    return kwargs.get('message', '새 알림이 있습니다.')

def trigger_notification(event_type, user, **kwargs):
    """이벤트 발생 시 알림 트리거"""
    message = get_notification_message(event_type, **kwargs)
    return create_notification(user, message, notif_type=event_type)

def should_notify(event):

    return True 