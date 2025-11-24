from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'payment_method', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentDetailSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='booking.id', read_only=True)
    booking_status = serializers.CharField(source='booking.status', read_only=True)
    passenger_username = serializers.CharField(source='booking.passenger.username', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'booking_id', 'booking_status', 'passenger_username',
            'amount', 'payment_method', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
