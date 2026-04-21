from sqlalchemy import Column, Integer, String
from .database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    destination = Column(String)
    date = Column(String)
    train_number = Column(String)
    ticket_class = Column(String)