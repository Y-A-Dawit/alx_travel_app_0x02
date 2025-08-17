# listings/tasks.py

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def sample_task():
    print("This is a test task from Celery")
    return "Task complete"

@shared_task
def send_payment_confirmation_email(user_email, booking_id):
    send_mail(
        subject="Payment Confirmation",
        message=f"Your payment for booking {booking_id} was successful.",
        from_email="noreply@travelapp.com",
        recipient_list=[user_email],
    )