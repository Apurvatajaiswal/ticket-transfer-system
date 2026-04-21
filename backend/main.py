from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, SessionLocal, Base
from .import models
from backend.schemas import TicketCreate, TicketResponse
import razorpay

app = FastAPI()

# 🔑 Razorpay client
client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_SECRET"))

@app.post("/create-order")
def create_order(data: dict):
    amount = data["amount"] * 100  # rupees → paise

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return order
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# test route
@app.get("/")
def home():
    return {"message": "Ticket Transfer API running"}


# get all tickets

@app.get("/tickets", response_model=list[TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    return db.query(models.Ticket).all()


# upload ticket
@app.post("/upload-ticket")
def upload_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = models.Ticket(
        train=ticket.train,
        source=ticket.source,
        destination=ticket.destination,
        seat=ticket.seat
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# search ticket
@app.get("/search-ticket")
def search_ticket(source: str, destination: str, db: Session = Depends(get_db)):

    tickets = db.query(models.Ticket).filter(
        models.Ticket.source == source,
        models.Ticket.destination == destination
    ).all()

    return tickets


# delete / claim ticket
@app.delete("/delete-ticket/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):

    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": "Ticket not found"}

    db.delete(ticket)
    db.commit()



