from django.urls import path
from .views import saisir_notes, admin_notes, teacher_courses

urlpatterns = [
    #path('saisir/<int:course_id>/', saisir_notes, name='saisir_notes'),
    path('admin-notes/', admin_notes),
    # Correct
    path('notes/saisir/<int:assignment_id>/', saisir_notes, name='saisir_notes'),
    path('mes-cours/', teacher_courses, name='teacher_courses')
]