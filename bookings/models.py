from django.conf import settings
from django.db import models
from vehicles.models import Vehicle
from django_google_maps.fields import AddressField, GeoLocationField
from core.models import SoftDeleteModel

class Booking(SoftDeleteModel):
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
    pickup_location = models.CharField(max_length=200)
    pickup_location_gmap = AddressField(max_length=200, blank=True, null=True)
    pickup_location_coordinates = GeoLocationField(max_length=100, blank=True, null=True)
    dropoff_location = models.CharField(max_length=200)
    dropoff_location_gmap = AddressField(max_length=200, blank=True, null=True)
    dropoff_location_coordinates = GeoLocationField(max_length=100, blank=True, null=True)
    pickup_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} - {self.passenger.username}"
