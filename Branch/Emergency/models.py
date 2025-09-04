from django.db import models

class BackgroundImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='backgrounds/')

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)  
    city = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    doctor_name = models.CharField(max_length=100)
    reason = models.TextField()
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.doctor_name}"
