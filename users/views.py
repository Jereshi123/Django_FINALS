from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserListSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'role']
    ordering_fields = ['username', 'role', 'created_at']
    ordering = ['username']

    def get_serializer_class(self):
        """Use UserListSerializer for list views"""
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer

    def get_permissions(self):
        """Allow registration without auth, restrict others"""
        if self.action == 'register':
            return [permissions.AllowAny()]
        elif self.action in ['profile', 'change_password']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Non-admin users can only view other users (not private data)"""
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        # Regular users see list of drivers/passengers, not full details
        return User.objects.all()

    # Endpoint: POST /api/users/register/
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register new user and return JWT tokens"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint: GET /api/users/profile/
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    # Endpoint: PUT /api/users/profile/
    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint: POST /api/users/change-password/
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return Response(
                {"error": "old_password, new_password, and confirm_password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"error": "New passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(new_password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        
        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete"""
        instance.soft_delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def restore(self, request, pk=None):
        """Restore a soft-deleted user"""
        user = User.objects.all_with_deleted().get(pk=pk)
        if user.is_deleted():
            user.restore()
            return Response({'status': 'User restored'})
        return Response({'status': 'User is not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint: GET /api/users/drivers/
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def drivers(self, request):
        """Get list of all drivers"""
        drivers = User.objects.filter(role='DRIVER')
        serializer = UserListSerializer(drivers, many=True)
        return Response(serializer.data)

    # Endpoint: GET /api/users/passengers/
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def passengers(self, request):
        """Get list of all passengers (admin only)"""
        passengers = User.objects.filter(role='PASSENGER')
        serializer = UserListSerializer(passengers, many=True)
        return Response(serializer.data)