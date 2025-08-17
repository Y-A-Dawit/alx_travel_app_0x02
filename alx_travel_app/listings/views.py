from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking, Payment
from .services.chapa import initiate_payment, verify_payment
from .tasks import send_payment_confirmation_email

# Create your views here.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_payment_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

    callback_url = "http://127.0.0.1:8000/api/payments/verify/"
    data, tx_ref = initiate_payment(booking, callback_url)

    if data.get("status") == "success":
        Payment.objects.create(
            booking=booking, tx_ref=tx_ref, amount=booking.total_price, status="pending"
        )
        return Response({"payment_url": data["data"]["checkout_url"]})
    return Response({"error": "Payment initiation failed"}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_payment_view(request):
    tx_ref = request.query_params.get("tx_ref")
    if not tx_ref:
        return Response({"error": "Transaction reference required"}, status=400)

    data = verify_payment(tx_ref)
    try:
        payment = Payment.objects.get(tx_ref=tx_ref)
        if data.get("status") == "success" and data["data"]["status"] == "success":
            payment.status = "completed"
            payment.save()
            send_payment_confirmation_email.delay(payment.booking.user.email, payment.booking.id)
            return Response({"message": "Payment successful"})
        else:
            payment.status = "failed"
            payment.save()
            return Response({"message": "Payment failed"})
    except Payment.DoesNotExist:
        return Response({"error": "Invalid transaction reference"}, status=404)
    
def api_overview(request):
    return JsonResponse({'message': 'Welcome to the Listings API'})

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer