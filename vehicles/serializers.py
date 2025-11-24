from rest_framework import serializers
from .models import Vehicle
from users.serializers import UserListSerializer

class VehicleSerializer(serializers.ModelSerializer):
    driver_details = UserListSerializer(source='driver', read_only=True, allow_null=True)
    
    class Meta:
        model = Vehicle
        fields = ['id', 'driver', 'driver_details', 'plate_number', 'model', 'status']
        read_only_fields = ['id']
