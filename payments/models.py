from django.db import models
from academics.models import Student

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    reference = models.CharField(max_length=255, blank=True, null=True)

    STATUS_CHOICES = [
        ('VALID', 'Validé'),
        ('PENDING', 'En attente'),
        ('ERROR', 'Erreur'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='VALID')

    raw_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.amount}"