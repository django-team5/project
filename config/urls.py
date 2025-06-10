from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('transactions/', include('apps.transactions.urls')),
    path('analysis/', include('apps.analysis.urls')),
    path('notifications/', include('apps.notifications.urls')),
] 