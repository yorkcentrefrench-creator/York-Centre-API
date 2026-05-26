import os
from dotenv import load_dotenv

# Load .env file in development, but don't fail if it doesn't exist (Render won't have it)
load_dotenv(override=False)

# Email Configuration
# Set EMAIL_ENABLED=false on Render to disable email sending entirely.
# If EMAIL_ENABLED=true, the app will attempt to send demo request emails via Brevo.
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME", "YorkCentre")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").strip().lower() in ["1", "true", "yes"]

# Payment Configuration
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")