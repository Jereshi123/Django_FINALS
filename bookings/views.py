from rest_framework import viewsets, permissions, status, serializers, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Booking
from .serializers import BookingSerializer, BookingListSerializer
from vehicles.models import Vehicle

User = get_user_model()

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'pickup_time', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use lightweight serializer for list views"""
        if self.action == 'list':
            return BookingListSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        passenger = self.request.user
        
        # Find available driver (first driver not on trip)
        available_driver = User.objects.filter(
            role='DRIVER',
            driver_bookings__status__in=['PENDING', 'ACCEPTED', 'ONGOING']
        ).exclude(
            id__in=Booking.objects.filter(
                status__in=['ONGOING']
            ).values_list('driver_id', flat=True)
        ).first()
        
        if not available_driver:
            raise serializers.ValidationError("No available drivers at the moment.")
        
        # Find available vehicle
        available_vehicle = Vehicle.objects.filter(status='AVAILABLE').first()
        if not available_vehicle:
            raise serializers.ValidationError("No available vehicles at the moment.")
        
        # Save booking
        booking = serializer.save(
            passenger=passenger,
            driver=available_driver,
            vehicle=available_vehicle,
            status='PENDING'
        )
        
        # Mark vehicle as on trip
        available_vehicle.status = 'ON_TRIP'
        available_vehicle.save()

    def get_queryset(self):
        """Filter bookings based on user role"""
        user = self.request.user
        if user.role == 'PASSENGER':
            return Booking.objects.filter(passenger=user)
        elif user.role == 'DRIVER':
            return Booking.objects.filter(driver=user)
        # Admin sees all
        return Booking.objects.all()

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        """Restore a soft-deleted booking"""
        booking = Booking.objects.all_with_deleted().get(pk=pk)
        if booking.is_deleted():
            booking.restore()
            return Response({'status': 'Booking restored'})
        return Response({'status': 'Booking is not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint: PATCH /api/bookings/{id}/accept/
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        """Driver accepts a booking"""
        booking = self.get_object()
        
        # Only driver can accept
        if booking.driver != request.user:
            return Response(
                {"error": "Only assigned driver can accept this booking"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status != 'PENDING':
            return Response(
                {"error": f"Cannot accept booking with status {booking.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'ACCEPTED'
        booking.save()
        return Response(
            self.get_serializer(booking).data,
            status=status.HTTP_200_OK
        )

    # Endpoint: PATCH /api/bookings/{id}/start/
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def start(self, request, pk=None):
        """Driver starts the trip"""
        booking = self.get_object()
        
        if booking.driver != request.user:
            return Response(
                {"error": "Only assigned driver can start this trip"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status != 'ACCEPTED':
            return Response(
                {"error": f"Trip can only be started from ACCEPTED status"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'ONGOING'
        booking.save()
        return Response(
            self.get_serializer(booking).data,
            status=status.HTTP_200_OK
        )

    # Endpoint: PATCH /api/bookings/{id}/complete/
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def complete(self, request, pk=None):
        """Driver completes the trip"""
        booking = self.get_object()
        
        if booking.driver != request.user:
            return Response(
                {"error": "Only assigned driver can complete this trip"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status != 'ONGOING':
            return Response(
                {"error": "Only ongoing trips can be completed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'COMPLETED'
        booking.save()
        
        # Mark vehicle as available
        if booking.vehicle:
            booking.vehicle.status = 'AVAILABLE'
            booking.vehicle.save()
        
        return Response(
            self.get_serializer(booking).data,
            status=status.HTTP_200_OK
        )

    # Endpoint: PATCH /api/bookings/{id}/cancel/
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        # Passenger or Driver can cancel (not completed/cancelled)
        if booking.passenger != request.user and booking.driver != request.user:
            return Response(
                {"error": "Only passenger or driver can cancel this booking"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status in ['COMPLETED', 'CANCELLED']:
            return Response(
                {"error": f"Cannot cancel booking with status {booking.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'CANCELLED'
        booking.save()
        
        # Release vehicle
        if booking.vehicle:
            booking.vehicle.status = 'AVAILABLE'
            booking.vehicle.save()
        
        return Response(
            self.get_serializer(booking).data,
            status=status.HTTP_200_OK
        )