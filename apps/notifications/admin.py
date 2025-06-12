from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    # 2025-06-12: 현재 모델의 실제 필드에 맞게 수정 (user, type 필드 없음으로 인한 에러 해결)
    list_display = ['id', 'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    # 원래 설정 (모델에 user, type 필드 추가 시 복원용)
    # list_display = ['id', 'user', 'message', 'type', 'is_read', 'created_at']
    # list_filter = ['type', 'is_read', 'created_at']
    # search_fields = ['message', 'user__email'] 