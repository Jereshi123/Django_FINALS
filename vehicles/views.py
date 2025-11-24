from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['plate_number', 'model']
    ordering_fields = ['status', 'model']
    ordering = ['plate_number']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]  # Only admins can modify
        return [permissions.IsAuthenticated()]  # Authenticated users can view

    def get_queryset(self):
        """Filter vehicles by status if requested"""
        queryset = Vehicle.objects.all()
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete"""
        instance.soft_delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def restore(self, request, pk=None):
        """Restore a soft-deleted vehicle"""
        vehicle = Vehicle.objects.all_with_deleted().get(pk=pk)
        if vehicle.is_deleted():
            vehicle.restore()
            return Response({'status': 'Vehicle restored'})
        return Response({'status': 'Vehicle is not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint: GET /api/vehicles/available/
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def available(self, request):
        """Get all available vehicles"""
        available_vehicles = Vehicle.objects.filter(status='AVAILABLE')
        serializer = self.get_serializer(available_vehicles, many=True)
        return Response(serializer.data)

    # Endpoint: GET /api/vehicles/{id}/update-status/
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        """Admin endpoint to update vehicle status"""
        vehicle = self.get_object()
        new_status = request.data.get('status')
        
        valid_statuses = ['AVAILABLE', 'ON_TRIP', 'MAINTENANCE']
        if new_status not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Must be one of {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        vehicle.status = new_status
        vehicle.save()
        return Response(self.get_serializer(vehicle).data)
