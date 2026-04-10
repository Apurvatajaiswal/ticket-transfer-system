from sqlalchemy import Column, Integer, String
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    train = Column(String)
    source = Column(String)
    destination = Column(String)
    seat = Column(String)