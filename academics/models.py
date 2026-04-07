from django.db import models

# -----------------------------
# SECTION (Informatique, Finance...)
# -----------------------------
class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -----------------------------
# PROMOTION (L1, L2, L3...)
# -----------------------------
class Promotion(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# -----------------------------
# SEMESTRE (S1, S2...)
# -----------------------------
class Semester(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# -----------------------------
# UE (Unité d'enseignement)
# -----------------------------
class UE(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    credit = models.IntegerField()

    def __str__(self):
        return f"{self.code} - {self.name}"

# DEPARTEMENT
# -----------------------------
class Department(models.Model):
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.section})"
# -----------------------------
# ETUDIANT
# -----------------------------
class Student(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)

    vacation = models.CharField(
        max_length=10,
        choices=[('jour', 'Jour'), ('soir', 'Soir')]
    )

    statut = models.CharField(
        max_length=20,
        choices=[
            ('actif', 'Actif'),
            ('abandon', 'Abandon'),
            ('exclu', 'Exclu'),
        ],
        default='actif'
    )

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"

# -----------------------------
