from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, SessionLocal, Base
from .import models

app = FastAPI()

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
@app.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    return db.query(models.Ticket).all()


# upload ticket
@app.post("/upload-ticket")
def upload_ticket(train: str, source: str, destination: str, seat: str, db: Session = Depends(get_db)):

    ticket = models.Ticket(
        train=train,
        source=source,
        destination=destination,
        seat=seat
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


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

    return {"message": "Ticket claimed"}