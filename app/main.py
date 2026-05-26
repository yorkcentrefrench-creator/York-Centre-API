import threading
import logging

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.payment import router as payment_router
from app.schemas import DemoRequest
from app.utils.email import send_demo_request_email

logger = logging.getLogger(__name__)

# Single FastAPI instance
app = FastAPI(title="York Centre API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(payment_router)

# Global variable to store email status
email_status = {"success": None, "message": None}

def send_email_background(name, email, mobile_number, message):
    """Background thread function to send email and store status"""
    global email_status
    success, msg = send_demo_request_email(name, email, mobile_number, message)
    email_status["success"] = success
    email_status["message"] = msg

@app.get("/")
def root():
    return {"status": "Payment API Running"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "York Centre API"}

# Demo booking endpoint
@app.post("/book-demo")
def book_demo(data: DemoRequest):
    """Submit a demo request and send email notification"""
    global email_status
    
    # Reset status
    email_status = {"success": None, "message": None}
    
    # Send email in background so the API responds instantly
    thread = threading.Thread(
        target=send_email_background,
        args=(data.name, data.email, data.mobile_number, data.message),
        daemon=False,  # Changed to False for better tracking
    )
    thread.start()
    thread.join(timeout=5)  # Wait max 5 seconds for email to send
    
    # Return status to client
    if email_status["success"] is False:
        raise HTTPException(
            status_code=500,
            detail=f"Email service error: {email_status['message']}"
        )

    if email_status["success"] is None:
        return {
            "message": "Demo request submitted successfully",
            "email_sent": False,
            "details": email_status["message"]
        }

    return {
        "message": "Demo request submitted successfully",
        "email_sent": True,
        "details": email_status["message"]
    }