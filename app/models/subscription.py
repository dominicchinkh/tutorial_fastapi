from datetime import datetime
from pydantic import BaseModel

class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime
