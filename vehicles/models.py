from django.db import models
from users.models import User
from core.models import SoftDeleteModel

class Vehicle(SoftDeleteModel):
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
    
        
    def __str__(self):
        # Use vehicle_type (previously named `model`) and handle None
        vtype = self.vehicle_type or 'Unknown'
        return f"{vtype} - {self.plate_number}"
