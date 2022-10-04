from django.urls import path
from .views import Health
from .views import AccountView
from .views import AccountDetailView

urlpatterns = [
    path('', Health.as_view(), name='health'),
    path('crear_cuenta/', AccountView.as_view()),
    path('detalle_cuenta/<int:id>', AccountDetailView.as_view())
]