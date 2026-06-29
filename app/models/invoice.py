from pydantic import BaseModel

class Invoice(BaseModel):
    id: str
    title: str | None = None
    customer: str
    total: float

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool
