from django.db import models

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    time_slots = [
        ('9:00','9:00'),
        ('10:00','10:00'),
        ('11:00','11:00'),
        ('12:00','12:00')
    ]

    patient_name = models.CharField(max_length = 100)
    email = models.EmailField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time_slot  = models.CharField(max_length=100,choices=time_slots)

    def __str__(self):
        return self.patient_name
