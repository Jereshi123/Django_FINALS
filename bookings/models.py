from django.conf import settings
from django.db import models
from vehicles.models import Vehicle

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='passenger_bookings')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='driver_bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    
    # Pickup Location
    pickup_location = models.CharField(max_length=200)
    pickup_geolocation = models.CharField(max_length=50, blank=False, null=False, default='0,0')
    
    # Dropoff Location
    dropoff_location = models.CharField(max_length=200)
    dropoff_geolocation = models.CharField(max_length=50, blank=False, null=False, default='0,0')
    
    pickup_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        try:
            return f"Booking {self.id} - {self.pickup_location} to {self.dropoff_location}"
        except Exception:
            return f"Booking {self.id}"
