import smtplib
import os
from email.message import EmailMessage

def send_demo_request_email(name: str, email: str, mobile_number: int, message: str):
    msg = EmailMessage()
    msg["Subject"] = "📩 New Demo Class Request"
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = os.getenv("ADMIN_EMAIL")

    msg.set_content(f"""
    New Demo Class Request Received
    
    Name: {name}
    Email: {email}
    Mobile Number: {mobile_number}
    Message:{message} """)

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(
            os.getenv("SMTP_USER"),
            os.getenv("SMTP_PASSWORD")
        )
        server.send_message(msg)