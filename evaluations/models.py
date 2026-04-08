from django.db import models
from academics.models import Student
from courses.models import Course


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    tp = models.FloatField(null=True, blank=True)
    interro = models.FloatField(null=True, blank=True)
    examen = models.FloatField(null=True, blank=True)

    def moyenne(self):
        if self.tp is not None and self.interro is not None and self.examen is not None:
            return (self.tp + self.interro + self.examen) / 3
        return 0

    moyenne.short_description = "Moyenne"
    
    note_finale = models.FloatField(null=True, blank=True)

    statut = models.CharField(
        max_length=10,
        choices=[
            ('normal', 'Normal'),
            ('ABS', 'Absent'),
        ],
        default='normal'
    )

    is_submitted = models.BooleanField(default=False)

    def calculer_note(self):
    # Gestion absence
        if self.statut == 'ABS':
            self.note_finale = None
            return

    # Vérification des valeurs
        if all(v is not None for v in [self.tp, self.interro, self.examen]):
            self.note_finale = round(
                (self.tp * 0.3) +
                (self.interro * 0.2) +
                (self.examen * 0.5),
            2
        )
        else:
            self.note_finale = None
    def est_eliminatoire(self):
        # règle simple (<5)
        return self.note_finale is not None and self.note_finale < 5

    def __str__(self):
        return f"{self.student} - {self.course}"