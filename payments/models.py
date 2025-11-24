from django.db import models
from bookings.models import Booking
from core.models import SoftDeleteModel

class Payment(SoftDeleteModel):
    payment_method_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Gcash', 'Gcash'),
        ('PayMaya', 'PayMaya'),
    ]

    status_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'), 
        ('Failed', 'Failed'),
    ]
          
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=payment_method_CHOICES)
    status = models.CharField(max_length=20, choices= status_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.status}"
