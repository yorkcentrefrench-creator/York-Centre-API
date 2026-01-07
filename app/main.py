from fastapi import FastAPI, HTTPException
from app.payment import router as payment_router
from app.schemas import DemoRequest
from app.utils.email import send_demo_request_email

# Single FastAPI instance
app = FastAPI(title="York Centre API")

# Include routers
app.include_router(payment_router)

@app.get("/")
def root():
    return {"status": "Payment API Running"}

# Demo booking endpoint
@app.post("/book-demo")
def book_demo(data: DemoRequest):
    try:
        send_demo_request_email(
            name=data.name,
            email=data.email,
            mobile_number=data.mobile_number,
            message=data.message
        )
        return {"message": "Demo request submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to submit demo request")