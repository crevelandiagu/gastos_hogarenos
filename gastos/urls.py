from django.urls import path
from django.conf.urls import url
from .views import Health
from .views import AccountView
from .views import AccountDetailView
from .views import TransactionView
from .views import TransactionInterAcountView

urlpatterns = [
    path('', Health.as_view(), name='health'),
    path('cuenta/', AccountView.as_view()),
    path('cuenta/<int:id_acount>/', AccountView.as_view()),
    path('detalle_cuenta/<int:id>', AccountDetailView.as_view()),
    path('detalle_cuenta/<int:id>/<str:date>/', AccountDetailView.as_view()),
    path('transacion/<int:id_acount>', TransactionView.as_view()),
    path('transacion_inter_acount/', TransactionInterAcountView.as_view()),
]