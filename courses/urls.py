from django.urls import path
from evaluations.views import saisir_notes
from .views import mes_cours

urlpatterns = [
    path("mes-cours/", mes_cours, name="mes_cours"),
    path("saisir/<int:assignment_id>/", saisir_notes, name="saisir_notes"),
]