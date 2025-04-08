from django.db import models

# Create your models here.
class Room(models.Model):
    number  = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.number
    
class Booking(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    room = models.OneToOneField(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name