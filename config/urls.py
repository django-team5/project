from django.contrib import admin
from django.urls import path, include
from apps.users.views import create_admin
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
    path('api/analysis/', include('apps.analysis.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('accounts/', include('allauth.urls')),
    
    # 실제 기능 페이지들
    path('app/accounts/', TemplateView.as_view(template_name='accounts/account_list.html'), name='account_list'),
    path('app/notifications/', TemplateView.as_view(template_name='notifications/notification_list.html'), name='notification_list'),
    
    path('create-superuser/', create_admin),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
