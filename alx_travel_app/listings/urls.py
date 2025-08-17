# listings/urls.py
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, initiate_payment_view, verify_payment_view

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path("payments/initiate/<int:booking_id>/", initiate_payment_view, name="initiate_payment"),
    path("payments/verify/", verify_payment_view, name="verify_payment"),
]
