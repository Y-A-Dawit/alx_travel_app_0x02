import requests, os, uuid

CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
BASE_URL = "https://api.chapa.co/v1/transaction"

def initiate_payment(booking, callback_url):
    tx_ref = str(uuid.uuid4())
    payload = {
        "amount": str(booking.total_price),
        "currency": "ETB",
        "tx_ref": tx_ref,
        "return_url": callback_url,
        "customization[title]": "Travel Booking Payment",
        "customization[description]": f"Payment for booking {booking.id}",
        "email": booking.user.email,
        "first_name": booking.user.first_name,
        "last_name": booking.user.last_name,
    }
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    response = requests.post(f"{BASE_URL}/initialize", json=payload, headers=headers)
    return response.json(), tx_ref

def verify_payment(tx_ref):
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    response = requests.get(f"{BASE_URL}/verify/{tx_ref}", headers=headers)
    return response.json()
