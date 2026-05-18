import threading

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.payment import router as payment_router
from app.schemas import DemoRequest
from app.utils.email import send_demo_request_email

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

@app.get("/")
def root():
    return {"status": "Payment API Running"}

# Demo booking endpoint
@app.post("/book-demo")
def book_demo(data: DemoRequest):
    # Send email in background so the API responds instantly
    thread = threading.Thread(
        target=send_demo_request_email,
        args=(data.name, data.email, data.mobile_number, data.message),
        daemon=True,
    )
    thread.start()
    return {"message": "Demo request submitted successfully"}