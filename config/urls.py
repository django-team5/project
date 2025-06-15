from django.contrib import admin
from django.urls import path, include
from apps.users.views import create_admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Ledger API",
        default_version='v1',
        description="가계부 백엔드 API 문서입니다.",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
    path('api/analysis/', include('apps.analysis.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('accounts/', include('allauth.urls')),
    path('create-superuser/', create_admin),
    path('api/analysis/', include('apps.analysis.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/test/', include('apps.test.urls')),
]
