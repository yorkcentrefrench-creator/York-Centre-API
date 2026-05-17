import os
import requests


def send_demo_request_email(name, email, mobile_number, message):
    api_key = os.getenv("BREVO_API_KEY")
    from_email = os.getenv("FROM_EMAIL")
    from_name = os.getenv("FROM_NAME", "YorkCentre")
    admin_email = os.getenv("ADMIN_EMAIL")

    html_content = f"""\
    <h3>New Demo Request</h3>
    <p><b>Name:</b> {name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Mobile:</b> {mobile_number}</p>
    <p><b>Message:</b><br>{message}</p>
    """

    payload = {
        "sender": {"name": from_name, "email": from_email},
        "to": [{"email": admin_email}],
        "subject": "New Demo Request",
        "htmlContent": html_content,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key,
    }

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=payload,
        headers=headers,
    )

    if response.status_code not in (200, 201):
        raise Exception(f"Brevo API error {response.status_code}: {response.text}")

    print(f"✅ Demo request email sent to {admin_email}")