from fastapi import APIRouter
from model.schemas.daily_finance import DailyFinanceBase, DailyFinanceRead, DailyFinanceCreate
import service.daily_finance as service

router = APIRouter(prefix="/api/daily_finances")

@router.get("/")
def get_all() -> list[DailyFinanceBase]:
    """Get all daily finances"""
    return service.get_all()    

@router.get("/{id}")
def get_one(id: int) -> DailyFinanceRead | None:
    """Get one daily finance by id"""
    return service.get_one(id)

@router.post("/")
def create(daily_finance: DailyFinanceCreate) -> DailyFinanceCreate | None:
    """Create a new daily finance (not implemented)"""  
    return service.create(daily_finance)

@router.delete("/{id}")
def delete(id: int) -> None:
    """Delete a daily finance (not implemented)"""
    return service.delete(id)