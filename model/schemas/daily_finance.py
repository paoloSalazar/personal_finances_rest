from pydantic import BaseModel
from datetime import date

class DailyFinanceBase(BaseModel):
    id: int | None = None
    date: date
    item: str
    amount: float
    type: str  # e.g., 'income' or 'expense'
    category_id: int
    payment_method: str
    observations: str | None = None

class DailyFinanceCreate(DailyFinanceBase):
    id: int | None = None
    
class DailyFinanceRead(DailyFinanceBase):
    id: int | None = None

    class Config:
        from_attributes = True