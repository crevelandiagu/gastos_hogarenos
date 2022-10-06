from django.urls import path
from .views import Health
from .views import AccountView
from .views import AccountDetailView
from .views import TransactionView

urlpatterns = [
    path('', Health.as_view(), name='health'),
    path('crear_cuenta/', AccountView.as_view()),
    path('detalle_cuenta/<int:id>', AccountDetailView.as_view()),
    path('transacion/<int:id_acount>', TransactionView.as_view()),

]