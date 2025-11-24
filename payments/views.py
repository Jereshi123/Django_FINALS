from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Payment
from .serializers import PaymentSerializer, PaymentDetailSerializer
from bookings.models import Booking

User = get_user_model()

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'amount', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use detailed serializer for detail views"""
        if self.action == 'retrieve':
            return PaymentDetailSerializer
        return PaymentSerializer

    def get_permissions(self):
        """Different permissions for different actions"""
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """Only allow creating payments for own bookings"""
        booking_id = serializer.initial_data.get('booking')
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            raise ValueError("Booking not found")
        
        # Only passenger can create payment for their booking
        if booking.passenger != self.request.user:
            raise PermissionError("You can only create payments for your own bookings")
        
        serializer.save()

    def get_queryset(self):
        """Filter payments based on user role"""
        user = self.request.user
        
        if user.is_staff:
            return Payment.objects.all()
        
        # Passenger sees payments for their bookings
        if user.role == 'PASSENGER':
            return Payment.objects.filter(booking__passenger=user)
        
        # Driver sees payments for their completed trips
        if user.role == 'DRIVER':
            return Payment.objects.filter(booking__driver=user)
        
        return Payment.objects.none()

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete"""
        instance.soft_delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def restore(self, request, pk=None):
        """Restore a soft-deleted payment"""
        payment = Payment.objects.all_with_deleted().get(pk=pk)
        if payment.is_deleted():
            payment.restore()
            return Response({'status': 'Payment restored'})
        return Response({'status': 'Payment is not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint: PATCH /api/payments/{id}/verify/
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def verify(self, request, pk=None):
        """Admin verifies a pending payment"""
        payment = self.get_object()
        
        if payment.status != 'Pending':
            return Response(
                {"error": f"Cannot verify payment with status {payment.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'Completed'
        payment.save()
        
        return Response(
            self.get_serializer(payment).data,
            status=status.HTTP_200_OK
        )

    # Endpoint: PATCH /api/payments/{id}/reject/
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """Admin rejects a pending payment"""
        payment = self.get_object()
        
        if payment.status != 'Pending':
            return Response(
                {"error": f"Cannot reject payment with status {payment.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'Failed'
        payment.save()
        
        return Response(
            self.get_serializer(payment).data,
            status=status.HTTP_200_OK
        )

    # Endpoint: GET /api/payments/by-booking/{booking_id}/
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def by_booking(self, request):
        """Get payment for a specific booking"""
        booking_id = request.query_params.get('booking_id')
        
        if not booking_id:
            return Response(
                {"error": "booking_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            payment = Payment.objects.get(booking_id=booking_id)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)
