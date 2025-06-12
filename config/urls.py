from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
    path('api/analysis/', include('apps.analysis.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('accounts/', include('allauth.urls')),
]
