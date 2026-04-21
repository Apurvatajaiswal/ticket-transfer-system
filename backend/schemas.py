from pydantic import BaseModel

class TicketCreate(BaseModel):
    train_number: str
    source: str
    destination: str
    date: str
    ticket_class: str

class TicketResponse(BaseModel):
    id: int
    train_number: str
    source: str
    destination: str
    date: str
    ticket_class: str

    class Config:
        orm_mode = True    