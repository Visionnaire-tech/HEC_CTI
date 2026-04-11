import pandas as pd
from django.shortcuts import render
from .models import Student, Promotion, Department
from django.contrib.auth.decorators import user_passes_test


def normalize(col):
    return col.strip().lower()


def import_students(request):
    if request.method == 'POST':
        file = request.FILES['file']

        df = pd.read_excel(file)

        # normaliser colonnes
        df.columns = [normalize(c) for c in df.columns]

        for _, row in df.iterrows():

            matricule = row.get('matricule') or row.get('id')
            nom = row.get('nom') or row.get('name')
            prenom = row.get('prenom') or row.get('firstname')

            promo_name = row.get('promotion') or row.get('classe')
            dept_name = row.get('department') or row.get('section')

            try:
                promo = Promotion.objects.get(name=promo_name)
                dept = Department.objects.get(name=dept_name)
            except:
                continue

            Student.objects.update_or_create(
                matricule=matricule,
                defaults={
                    'nom': nom,
                    'prenom': prenom,
                    'promotion': promo,
                    'department': dept,
                    'vacation': row.get('vacation', 'Jour')
                }
            )

        return render(request, 'academics/import_success.html')

    return render(request, 'academics/import_students.html')

def admin_required(user):
    return user.is_superuser


from academics.models import Promotion

def admin_home(request):
    promotions = Promotion.objects.all()

    return render(request, "deliberation/admin/home.html", {
        "promotions": promotions
    })
def admin_dashboard(request):
    promotions = Promotion.objects.all()
    return render(request, 'deliberation/admin/dashboard.html', {
        'promotions': promotions
    })


def admin_students(request):
    students = Student.objects.all()
    return render(request, 'deliberation/admin/students.html', {
        'students': students
    })


def admin_student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'deliberation/admin/student_detail.html', {
        'student': student
    })


def admin_courses(request):
    courses = Course.objects.all()
    return render(request, 'deliberation/admin/courses.html', {
        'courses': courses
    })


def admin_assignments(request):
    assignments = CourseAssignment.objects.select_related('teacher', 'course')
    return render(request, 'deliberation/admin/assignments.html', {
        'assignments': assignments
    })


def admin_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'deliberation/admin/teachers.html', {
        'teachers': teachers
    })


def admin_ues(request):
    ues = UE.objects.all()
    return render(request, 'deliberation/admin/ues.html', {
        'ues': ues
    })

