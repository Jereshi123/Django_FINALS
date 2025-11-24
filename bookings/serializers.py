from rest_framework import serializers
from .models import Booking
from users.serializers import UserSerializer
from vehicles.serializers import VehicleSerializer

class BookingSerializer(serializers.ModelSerializer):
    passenger_name = serializers.CharField(source='passenger.username', read_only=True)
    driver_name = serializers.CharField(source='driver.username', read_only=True, allow_null=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True, allow_null=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'passenger', 'passenger_name', 'driver', 'driver_name', 
            'vehicle', 'vehicle_details',
            'pickup_location', 'pickup_geolocation',
            'dropoff_location', 'dropoff_geolocation',
            'pickup_time', 'status', 'fare',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'passenger', 'status', 'fare', 'pickup_time', 'created_at']
