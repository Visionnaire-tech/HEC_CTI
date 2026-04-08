from django.shortcuts import render, get_object_or_404, redirect
from academics.models import Student, Promotion, Department
from django.contrib.auth.decorators import login_required
from courses.models import Course ,CourseAssignment
from .models import Grade

@login_required
def saisir_notes(request, assignment_id):
    # Récupère l'assignation du professeur correspondant à l'ID
    assignment = get_object_or_404(CourseAssignment, id=assignment_id)
    course = assignment.course  # <-- Correction ici

    # Étudiants de la promotion et du département
    students = Student.objects.filter(
        promotion=course.promotion,
        department=assignment.department
    )

    if request.method == "POST":
        for student in students:
            tp = request.POST.get(f"tp_{student.id}")
            interro = request.POST.get(f"interro_{student.id}")
            examen = request.POST.get(f"examen_{student.id}")
            statut = request.POST.get(f"statut_{student.id}")

            grade, created = Grade.objects.get_or_create(
                student=student,
                course=course
            )

            # Conversion des notes
            grade.tp = float(tp) if tp else None
            grade.interro = float(interro) if interro else None
            grade.examen = float(examen) if examen else None

            # Statut (Absent ou Normal)
            grade.statut = statut

            # Calcul automatique
            grade.calculer_note()
            grade.save()

        return redirect('/notes/mes-cours/')  # redirection directe vers l’URL

    return render(request, 'evaluations/saisir_notes.html', {
        'course': course,
        'students': students
    })


def admin_notes(request):
    promotions = Promotion.objects.all()
    departments = Department.objects.all()

    students = None
    courses = None
    data = []

    promo_id = request.GET.get('promotion')
    dept_id = request.GET.get('department')

    if promo_id and dept_id:
        students = Student.objects.filter(
            promotion_id=promo_id,
            department_id=dept_id
        )

        courses = Course.objects.filter(
            promotion_id=promo_id
        )

        for student in students:
            row = {
                'student': student,
                'notes': [],
                'moyenne': 0
            }

            total = 0
            coeff = 0

            for course in courses:
                try:
                    grade = Grade.objects.get(student=student, course=course)
                    note = grade.note_finale
                except Grade.DoesNotExist:
                    note = None

                row['notes'].append(note)

                if note is not None:
                    total += note * course.credit
                    coeff += course.credit

            row['moyenne'] = round(total / coeff, 2) if coeff else 0

            data.append(row)

    return render(request, 'evaluations/admin_notes.html', {
        'promotions': promotions,
        'departments': departments,
        'data': data,
        'courses': courses
    })
def teacher_courses(request):
    teacher = request.user.teacher

    courses = teacher.courseassignment_set.all()

    return render(request, "evaluations/teacher_courses.html", {
        "courses": courses
    })