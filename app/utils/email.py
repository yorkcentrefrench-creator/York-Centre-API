import os
import socket
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


def _resolve_ipv4(host, port):
    """Force IPv4 resolution — fixes '[Errno 101] Network is unreachable' on hosts without IPv6."""
    addr_info = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
    if not addr_info:
        raise OSError(f"Could not resolve {host} to an IPv4 address")
    return addr_info[0][4][0]  # returns the IPv4 IP string


def send_demo_request_email(name, email, mobile_number, message):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
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

    # Resolve to IPv4 to avoid IPv6 connectivity issues on cloud hosts
    ipv4_host = _resolve_ipv4(smtp_host, smtp_port)
    logger.info(f"Resolved {smtp_host} -> {ipv4_host} (IPv4)")

    if smtp_port == 465:
        # SSL
        with smtplib.SMTP_SSL(ipv4_host, smtp_port, timeout=10) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, admin_email, msg.as_string())
    else:
        # STARTTLS (port 587)
        with smtplib.SMTP(ipv4_host, smtp_port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, admin_email, msg.as_string())

    logger.info(f"✅ Demo request email sent to {admin_email}")