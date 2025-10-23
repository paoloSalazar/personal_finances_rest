from ..database import Base
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func

class DailyFinance(Base):
    __tablename__ = "daily_finances"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)
    item = Column(String(280), nullable=True)
    amount = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)  # e.g., 'income' or 'expense'
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)  # <- FK added
    payment_method = Column(String(50), nullable=True)
    observations = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())