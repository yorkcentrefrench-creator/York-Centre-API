import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_demo_request_email(name, email, mobile_number, message):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")
    from_name = os.getenv("FROM_NAME", "YorkCentre")
    admin_email = os.getenv("ADMIN_EMAIL")

    # Build the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "New Demo Request"
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = admin_email

    html_content = f"""\
    <h3>New Demo Request</h3>
    <p><b>Name:</b> {name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Mobile:</b> {mobile_number}</p>
    <p><b>Message:</b><br>{message}</p>
    """

    msg.attach(MIMEText(html_content, "html"))

    # Send via SMTP SSL (port 465)
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, admin_email, msg.as_string())

    print(f"✅ Demo request email sent to {admin_email}")