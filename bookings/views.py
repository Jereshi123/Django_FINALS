from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Booking
from .serializers import BookingSerializer, BookingListSerializer
from vehicles.models import Vehicle
from rest_framework import serializers

User = get_user_model()

class BookingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingSerializer
        return BookingListSerializer

    def perform_create(self, serializer):
        passenger = self.request.user
        available_driver = User.objects.filter(role='DRIVER').first()
        available_vehicle = Vehicle.objects.filter(status='AVAILABLE').first()
        
        if not available_driver or not available_vehicle:
            raise serializers.ValidationError("No available drivers or vehicles.")
        
        booking = serializer.save(
            passenger=passenger,
            driver=available_driver,
            vehicle=available_vehicle,
            status='PENDING'
        )
        return booking


class BookingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.soft_delete()


class BookingActionBase(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return None


class AcceptBookingAPIView(BookingActionBase):
    def post(self, request, pk):
        booking = self.get_booking(pk)
        if not booking:
            return Response({"error": "Booking not found"}, status=404)
        if booking.driver != request.user:
            return Response({"error": "Only assigned driver can accept"}, status=403)
        if booking.status != 'PENDING':
            return Response({"error": "Only PENDING bookings can be accepted"}, status=400)
        booking.status = 'ACCEPTED'
        booking.save()
        return Response(BookingSerializer(booking).data)


class StartBookingAPIView(BookingActionBase):
    def post(self, request, pk):
        booking = self.get_booking(pk)
        if not booking:
            return Response({"error": "Booking not found"}, status=404)
        if booking.driver != request.user:
            return Response({"error": "Only assigned driver can start"}, status=403)
        if booking.status != 'ACCEPTED':
            return Response({"error": "Only ACCEPTED bookings can be started"}, status=400)
        booking.status = 'ONGOING'
        booking.save()

        if booking.vehicle:
            booking.vehicle.status = 'ON_TRIP'
            booking.vehicle.save()
        return Response(BookingSerializer(booking).data)


class CompleteBookingAPIView(BookingActionBase):
    def post(self, request, pk):
        booking = self.get_booking(pk)
        if not booking:
            return Response({"error": "Booking not found"}, status=404)
        if booking.driver != request.user:
            return Response({"error": "Only assigned driver can complete"}, status=403)
        if booking.status != 'ONGOING':
            return Response({"error": "Only ONGOING bookings can be completed"}, status=400)
        booking.status = 'COMPLETED'
        booking.save()
        if booking.vehicle:
            booking.vehicle.status = 'AVAILABLE'
            booking.vehicle.save()
        return Response(BookingSerializer(booking).data)


class CancelBookingAPIView(BookingActionBase):
    def post(self, request, pk):
        booking = self.get_booking(pk)
        if not booking:
            return Response({"error": "Booking not found"}, status=404)
        if booking.passenger != request.user and booking.driver != request.user:
            return Response({"error": "Only passenger or driver can cancel"}, status=403)
        if booking.status in ['COMPLETED', 'CANCELLED']:
            return Response({"error": "Cannot cancel this booking"}, status=400)
        booking.status = 'CANCELLED'
        booking.save()
        if booking.vehicle:
            booking.vehicle.status = 'AVAILABLE'
            booking.vehicle.save()
        return Response(BookingSerializer(booking).data)