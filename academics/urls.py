from django.urls import path
from .views import import_students

urlpatterns = [
    path('import-students/', import_students),
]