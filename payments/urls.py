from django.urls import path
from . import views   # ✅ IMPORTANT

urlpatterns = [
    path('import/', views.import_payments_view, name='import_payments'),
]