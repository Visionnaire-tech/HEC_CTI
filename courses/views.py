from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CourseAssignment, Teacher


@login_required
def mes_cours(request):
    teacher = request.user.teacher

    assignments = CourseAssignment.objects.filter(teacher=teacher)

    return render(request, "courses/mes_cours.html", {
        "assignments": assignments
    })