import os
import requests

def send_demo_request_email(name, email, mobile_number, message):
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "email": os.getenv("FROM_EMAIL"),
            "name": os.getenv("FROM_NAME")
        },
        "to": [
            {"email": os.getenv("ADMIN_EMAIL")}
        ],
        "subject": "New Demo Request",
        "htmlContent": f"""
            <h3>New Demo Request</h3>
            <p><b>Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Mobile:</b> {mobile_number}</p>
            <p><b>Message:</b><br>{message}</p>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": os.getenv("BREVO_API_KEY"),
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code not in (200, 201):
        raise Exception(response.text)