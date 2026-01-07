import os
import smtplib
from email.message import EmailMessage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

ENV = os.getenv("ENV", "local")

def send_demo_request_email(name, email, mobile_number, message):
    content = f"""
        New Demo Request
        
        Name: {name}
        Email: {email}
        Mobile: {mobile_number}
        Message: {message}
        """
    if ENV == "local":
        msg = EmailMessage()
        msg["Subject"] = "New Demo Request"
        msg["From"] = os.getenv("SMTP_USER")
        msg["To"] = os.getenv("ADMIN_EMAIL")
        msg.set_content(content)

        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(
                os.getenv("SMTP_USER"),
                os.getenv("SMTP_PASSWORD")
            )
            server.send_message(msg)

    else:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        mail = Mail(
            from_email=os.getenv("FROM_EMAIL"),
            to_emails=os.getenv("ADMIN_EMAIL"),
            subject="New Demo Request",
            plain_text_content=content
        )
        sg.send(mail)
