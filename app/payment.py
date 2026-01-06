import os

import razorpay
from fastapi import APIRouter, HTTPException
from app.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from app.schemas import EnrollRequest
from app.utils.currency import get_cad_to_inr_rate
from fastapi import Request
from razorpay.errors import SignatureVerificationError
from app.config import RAZORPAY_WEBHOOK_SECRET

router = APIRouter(prefix="/payment", tags=["Payment"])

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)

PLANS_CAD = {
    "group": 270,
    "individual": 320,
    "intensive": 430
}

@router.post("/enroll")
def enroll(data: EnrollRequest):

    plan = data.plan.lower()
    if plan not in PLANS_CAD:
        raise HTTPException(status_code=400, detail="Invalid plan")

    cad_to_inr = get_cad_to_inr_rate()

    amount_cad = PLANS_CAD[plan]
    amount_inr = amount_cad * cad_to_inr
    amount_paise = int(amount_inr * 100)

    payment_link = client.payment_link.create({
        "amount": amount_paise,
        "currency": "INR",
        "description": f"{plan.title()} French Class Tuition",
        "customer": {
            "name": data.name,
            "email": data.email,
            "contact": data.phone
        },
        "notify": {
            "sms": True,
            "email": True
        },
        "callback_url": "https://yorkcentrefrench.com/payment-success",
        "callback_method": "get"
    })

    return {
        "plan": plan,
        "amount_cad": amount_cad,
        "conversion_rate": round(cad_to_inr, 2),
        "amount_inr": round(amount_inr, 2),
        "payment_url": payment_link["short_url"]
    }

@router.post("/webhook")
async def razorpay_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")

    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")

    try:
        client.utility.verify_webhook_signature(
            payload.decode(),
            signature,
            RAZORPAY_WEBHOOK_SECRET
        )
    except SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    data = await request.json()
    event = data.get("event")

    payment_entity = data["payload"]["payment"]["entity"]
    payment_id = payment_entity["id"]
    payment_link_id = payment_entity.get("payment_link_id")
    status = payment_entity["status"]

    if event == "payment_link.paid":
        print("PAYMENT SUCCESS")
        print("Payment ID:", payment_id)

    elif event == "payment_link.failed":
        print("PAYMENT FAILED")
        print("Payment ID:", payment_id)
        print("Reason:", payment_entity.get("error_description"))

    return {"status": "ok"}
