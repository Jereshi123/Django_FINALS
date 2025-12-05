"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Generic views from each app
from bookings.views import *
from vehicles.views import *
from payments.views import *
from users.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Bookings endpoints
    path('api/bookings/', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('api/bookings/<int:pk>/', BookingRetrieveUpdateDestroyAPIView.as_view(), name='booking-detail'),
    path('api/bookings/<int:pk>/accept/', AcceptBookingAPIView.as_view(), name='booking-accept'),
    path('api/bookings/<int:pk>/start/', StartBookingAPIView.as_view(), name='booking-start'),
    path('api/bookings/<int:pk>/complete/', CompleteBookingAPIView.as_view(), name='booking-complete'),
    path('api/bookings/<int:pk>/cancel/', CancelBookingAPIView.as_view(), name='booking-cancel'),
    path('api/bookings/restore/<int:pk>/', RestoreBookingAPIView.as_view(), name='booking-restore'),
    
    # Vehicles endpoints
    path('api/vehicles/', VehicleListCreateAPIView.as_view(), name='vehicle-list-create'),
    path('api/vehicles/<int:pk>/', VehicleRetrieveUpdateDestroyAPIView.as_view(), name='vehicle-detail'),
    path('api/vehicles/available/', AvailableVehiclesAPIView.as_view(), name='vehicle-available'),
    path('api/vehicles/<int:pk>/status/', UpdateVehicleStatusAPIView.as_view(), name='vehicle-update-status'),
    
    # Payments endpoints
    path('api/payments/', PaymentListCreateAPIView.as_view(), name='payment-list-create'),
    path('api/payments/<int:pk>/', PaymentRetrieveUpdateDestroyAPIView.as_view(), name='payment-detail'),
    path('api/payments/<int:pk>/verify/', VerifyPaymentAPIView.as_view(), name='payment-verify'),
    path('api/payments/<int:pk>/reject/', RejectPaymentAPIView.as_view(), name='payment-reject'),
    
    # Users endpoints
    path('api/users/register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('api/users/', UserListAPIView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('api/users/profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('api/users/change-password/', ChangePasswordAPIView.as_view(), name='user-change-password'),
    path('api/users/drivers/', DriverListAPIView.as_view(), name='user-drivers'),
    path('api/users/passengers/', PassengerListAPIView.as_view(), name='user-passengers'),
    path('api/passengers/', PassengerListAPIView.as_view(), name='passengers'),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


