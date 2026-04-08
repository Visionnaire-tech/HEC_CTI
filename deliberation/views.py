from django.shortcuts import render, redirect
from academics.models import Student, UE
from evaluations.models import Grade
from .services import calcul_deliberation

def admin_deliberation_view(request, promotion_id):
    students = Student.objects.filter(promotion_id=promotion_id)
    ues = UE.objects.filter(promotion_id=promotion_id)

    result = []

    for student in students:
        student_data = {
            "student": student,
            "ues": [],
            "total_credits": 0,
            "moyenne_generale": 0
        }

        total_points = 0
        total_coeff = 0

        for ue in ues:
            courses = ue.course_set.all()

            ue_total = 0
            ue_coeff = 0
            ue_courses = []

            for course in courses:
                grade = Grade.objects.filter(
                    student=student,
                    course=course
                ).first()

                moyenne = grade.moyenne if grade else 0

                ue_courses.append({
                    "course": course,
                    "note": moyenne
                })

                ue_total += moyenne * course.credit
                ue_coeff += course.credit

            ue_moyenne = ue_total / ue_coeff if ue_coeff > 0 else 0

            # Validation crédit
            if ue_moyenne >= 11:
                student_data["total_credits"] += ue.credit

            total_points += ue_total
            total_coeff += ue_coeff

            student_data["ues"].append({
                "ue": ue,
                "courses": ue_courses,
                "moyenne": round(ue_moyenne, 2)
            })

        moyenne_generale = total_points / total_coeff if total_coeff > 0 else 0
        student_data["moyenne_generale"] = round(moyenne_generale, 2)

        result.append(student_data)

    return render(request, "deliberation/admin_table.html", {
        "result": result
    })

def student_login(request):
    if request.method == "POST":
        matricule = request.POST.get("matricule")

        try:
            student = Student.objects.get(matricule=matricule)
            request.session['student_id'] = student.id
            return redirect('student_dashboard')
        except Student.DoesNotExist:
            return render(request, 'deliberation/student_login.html', {
                'error': 'Matricule incorrect'
            })

    return render(request, 'deliberation/student_login.html')


def student_dashboard(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)

    return render(request, 'deliberation/student_dashboard.html', {
        'student': student
    })




def student_result(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)

    result = calcul_deliberation(student)

    return render(request, 'deliberation/student_result.html', result)

from django.contrib.auth import logout

def custom_logout(request):
    # 🔴 Déconnexion Django (enseignant/admin)
    logout(request)

    # 🔴 Suppression session étudiant
    if 'student_id' in request.session:
        del request.session['student_id']

    return redirect('student_login')  # ou 'home'