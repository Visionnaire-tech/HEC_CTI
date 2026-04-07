from django.urls import path
from .views import mes_cours

urlpatterns = [
    path('mes-cours/', mes_cours),
]