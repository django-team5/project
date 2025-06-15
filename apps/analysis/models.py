from django.db import models
from django.conf import settings

class Analysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=10)  # '수입' 또는 '지출'
    period_type = models.CharField(max_length=10)  # '일간', '월간' 등
    start_date = models.DateField()
    end_date = models.DateField()
    summary = models.TextField()
    result_image_url = models.ImageField(upload_to='analysis/')  # 결과 그래프 이미지 저장
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.target_type} 분석 ({self.period_type})"