from django.db import models
from users.models import User

class Vehicle(models.Model):
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('ON_TRIP', 'On Trip'),
        ('MAINTENANCE', 'Maintenance'),
    )

    VEHICLE_CHOICES = (
        ('Car', 'Car'),
        ('Motorcycle', 'Motorcycle'),
        ('Van', 'Van'),
    )

    driver = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'DRIVER'})
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES, null=True)
    plate_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
        
    def __str__(self):
        try:
            return f"{self.vehicle_type} - {self.plate_number} (Driver: {self.driver.username})"
        except Exception:
            return f"{self.vehicle_type} - {self.plate_number}"
