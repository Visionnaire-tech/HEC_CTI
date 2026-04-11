from django.shortcuts import render, redirect
from academics.models import Student, UE
from evaluations.models import Grade
from .services import calcul_deliberation

from django.http import HttpResponse
from .export_excel import export_deliberation_excel

from .pdf import generate_student_pdf
import os


def student_pdf_view(request, student_id):
    student = Student.objects.get(id=student_id)

    file_path = f"bulletin_{student.id}.pdf"

    generate_student_pdf(student, file_path)

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="bulletin_{student.id}.pdf"'
        return response

def export_excel_view(request, promotion_id):
    students = Student.objects.filter(promotion_id=promotion_id)

    wb = export_deliberation_excel(students)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=deliberation.xlsx'

    wb.save(response)
    return response

from django.shortcuts import render
from academics.models import Student, UE
from evaluations.models import Grade


def admin_deliberation_view(request, promotion_id):
    students = Student.objects.filter(promotion_id=promotion_id)
    ues = UE.objects.filter(promotion_id=promotion_id).prefetch_related('course_set')

    data = []

    for student in students:
        row = {
            "student": student,
            "ues": [],
            "total_tnp": 0,
            "total_credit": 0,
            "moyenne": 0,
            "decision": ""
        }

        for ue in ues:
            courses = ue.course_set.all()

            ue_tnp = 0
            ue_credit = 0
            ue_courses = []

            for course in courses:
                grade = Grade.objects.filter(student=student, course=course).first()

                note = grade.note_finale if grade and grade.note_finale is not None else 0
                tnp = note * course.credit

                ue_tnp += tnp
                ue_credit += course.credit

                ue_courses.append({
                    "course": course,
                    "note": round(note, 2),
                    "tnp": round(tnp, 2)
                })

            ue_moyenne = ue_tnp / ue_credit if ue_credit else 0

            row["total_tnp"] += ue_tnp
            row["total_credit"] += ue_credit

            row["ues"].append({
                "ue": ue,
                "courses": ue_courses,
                "moyenne": round(ue_moyenne, 2),
                "tnp": round(ue_tnp, 2)
            })

        # moyenne générale
        row["moyenne"] = row["total_tnp"] / row["total_credit"] if row["total_credit"] else 0

        # décision
        if row["moyenne"] >= 11:
            row["decision"] = "ADM"
        elif row["moyenne"] >= 8:
            row["decision"] = "AJ"
        else:
            row["decision"] = "DEF"

        data.append(row)

    return render(request, "deliberation/admin_table.html", {
        "students_data": data,
        "ues": ues
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