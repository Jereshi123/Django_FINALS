from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer, PaymentDetailSerializer
from bookings.models import Booking


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        if user.role == 'PASSENGER':
            return Payment.objects.filter(booking__passenger=user)
        if user.role == 'DRIVER':
            return Payment.objects.filter(booking__driver=user)
        return Payment.objects.none()

    def perform_create(self, serializer):
        booking_id = serializer.initial_data.get('booking')
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            raise ValueError("Booking not found")
        
        if booking.passenger != self.request.user:
            raise PermissionError("You can only create payments for your own bookings")
        
        serializer.save()


class PaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentDetailSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_destroy(self, instance):
        instance.soft_delete()


class VerifyPaymentAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if payment.status != 'Pending':
            return Response(
                {"error": f"Cannot verify payment with status {payment.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'Completed'
        payment.save()
        return Response(PaymentDetailSerializer(payment).data)


class RejectPaymentAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if payment.status != 'Pending':
            return Response(
                {"error": f"Cannot reject payment with status {payment.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'Failed'
        payment.save()
        return Response(PaymentDetailSerializer(payment).data)
