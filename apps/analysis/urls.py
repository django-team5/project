from django.urls import path
from .views import AnalysisView, AnalysisListView

urlpatterns = [
    path('', AnalysisView.as_view(), name='analysis'),
    path('', AnalysisView.as_view(), name='analysis-create'),        # 생성용
    path('list/', AnalysisListView.as_view(), name='analysis-list'), # 리스트 조회용
]
