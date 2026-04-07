import pandas as pd
from django.shortcuts import render
from .models import Student, Promotion, Department


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