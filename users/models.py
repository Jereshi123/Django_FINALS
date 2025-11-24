from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import SoftDeleteModel

class User(AbstractUser, SoftDeleteModel):
    ROLE_CHOICES = [
        ('PASSENGER', 'Passenger'),
        ('DRIVER', 'Driver'),
        ('ADMIN', 'Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PASSENGER')
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"