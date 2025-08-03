# listings/urls.py
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
]
