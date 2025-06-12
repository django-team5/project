from django.urls import path
from .views import AnalysisView

# 분석 URL 패턴
urlpatterns = [
    path('', AnalysisView.as_view(), name='analysis'),
] 

# analysis 앱의 URLConf (예시)
urlpatterns = [] 