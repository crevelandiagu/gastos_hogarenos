
from django.contrib import admin
from django.urls import path
from django.urls import include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from gastos.views import Health

schema_view = get_schema_view(
    openapi.Info(
        title="Gastos Hogarenos",
        default_version="v1",
        description="Documentacion api",
        contact=openapi.Contact(email="crevelandiagu@unal.edu.co"),

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    )

urlpatterns = [
    path('', Health.as_view(), name='health'),
    path('admin/', admin.site.urls),
    path('api/', include('gastos.urls')),
    path('swagger/', schema_view.with_ui(
    'swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui(
    'redoc', cache_timeout=0)),
]
