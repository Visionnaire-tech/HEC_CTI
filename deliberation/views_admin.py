from django.shortcuts import render
from academics.models import Student, Promotion, Section, Department
from .services import calcul_deliberation


def admin_dashboard(request):
    promotions = Promotion.objects.all()
    sections = Section.objects.all()
    departments = Department.objects.all()

    return render(request, 'deliberation/admin/dashboard.html', {
        'promotions': promotions,
        'sections': sections,
        'departments': departments
    })


def admin_students(request):
    promotion_id = request.GET.get('promotion')
    section_id = request.GET.get('section')
    department_id = request.GET.get('department')

    students = Student.objects.all()

    # Filtrage par promotion
    if promotion_id:
        students = students.filter(promotion_id=promotion_id)

    # Filtrage par département
    if department_id:
        students = students.filter(department_id=department_id)

    # Filtrage par section via le département
    if section_id:
        students = students.filter(department__section_id=section_id)

    results = []

    for student in students:
        res = calcul_deliberation(student)

        results.append({
            'student': student,
            'moyenne': res['moyenne'],
            'credits': res['credits'],
            'decision': res['decision']
        })

    return render(request, 'deliberation/admin/students.html', {
        'results': results
    })


def admin_student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    result = calcul_deliberation(student)

    return render(request, 'deliberation/admin/student_detail.html', {
        'student': student,
        'result': result
    })


def admin_deliberation_global(request):
    students = Student.objects.all()

    for student in students:
        calcul_deliberation(student)

    return render(request, 'deliberation/admin/done.html')