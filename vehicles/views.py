from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class VehicleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_destroy(self, instance):
        instance.soft_delete()


class AvailableVehiclesAPIView(generics.ListAPIView):
    queryset = Vehicle.objects.filter(status='AVAILABLE')
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateVehicleStatusAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found"}, status=404)

        new_status = request.data.get('status')
        valid_statuses = ['Available', 'On Trip', 'Maintenance']
        
        if new_status not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Must be one of {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        vehicle.status = new_status
        vehicle.save()
        return Response(VehicleSerializer(vehicle).data)
