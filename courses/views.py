from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CourseAssignment, Teacher

@login_required
def mes_cours(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        assignments = CourseAssignment.objects.filter(teacher=teacher)
    except Teacher.DoesNotExist:
        assignments = []

    return render(request, 'courses/mes_cours.html', {
        'assignments': assignments
    })