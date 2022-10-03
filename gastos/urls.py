from django.urls import path
from .views import Health
from .views import AccountView

urlpatterns = [
    path('', Health.as_view(), name='health'),
    path('crear_cuenta/', AccountView.as_view())
]