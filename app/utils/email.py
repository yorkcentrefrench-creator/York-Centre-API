import logging
import requests
from app.config import BREVO_API_KEY, FROM_EMAIL, FROM_NAME, ADMIN_EMAIL, EMAIL_ENABLED

logger = logging.getLogger(__name__)

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_demo_request_email(name, email, mobile_number, message):
    """Send demo request email via Brevo HTTP API.
    Render blocks all SMTP ports, so we use Brevo's HTTPS API instead.

    Returns:
        tuple: (success: bool|None, message: str)
            - True: email sent
            - False: email was configured but sending failed
            - None: email sending disabled or not configured
    """

    if not EMAIL_ENABLED:
        info_msg = "Email sending is disabled by configuration. Demo request accepted without sending email."
        logger.info(info_msg)
        return None, info_msg

    # Validate required configuration
    missing_config = []
    if not BREVO_API_KEY:
        missing_config.append("BREVO_API_KEY")
    if not FROM_EMAIL:
        missing_config.append("FROM_EMAIL")
    if not ADMIN_EMAIL:
        missing_config.append("ADMIN_EMAIL")

    if missing_config:
        error_msg = f"Email configuration missing: {', '.join(missing_config)}. Set these in Render environment variables or disable email with EMAIL_ENABLED=false."
        logger.error(error_msg)
        return False, error_msg

    html_content = f"""\
    <h3>New Demo Request</h3>
    <p><b>Name:</b> {name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Mobile:</b> {mobile_number}</p>
    <p><b>Message:</b><br>{message}</p>
    """

    payload = {
        "sender": {"name": FROM_NAME, "email": FROM_EMAIL},
        "to": [{"email": ADMIN_EMAIL, "name": "Admin"}],
        "subject": "New Demo Request",
        "htmlContent": html_content,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY,
    }

    try:
        response = requests.post(BREVO_API_URL, json=payload, headers=headers, timeout=10)
        if response.status_code == 201:
            success_msg = f"Email sent to {ADMIN_EMAIL}"
            logger.info(f"✅ {success_msg}")
            return True, success_msg
        else:
            error_msg = f"Brevo API error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return False, error_msg
    except requests.Timeout:
        error_msg = "Email send timeout - Brevo API not responding"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Email send failed: {str(e)}"
        logger.error(error_msg)
        return False, error_msg