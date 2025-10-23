from model.schemas.daily_finance import DailyFinanceBase, DailyFinanceCreate, DailyFinanceRead
import data.daily_finance as data

def get_all() -> list[DailyFinanceRead]:
    """return all daily finances"""
    return data.get_all()

def get_one(id: int) -> DailyFinanceRead | None:
    """return one daily finance by id"""
    return data.get_one(id)

## Non functional methods
def create(daily_finance: DailyFinanceCreate) -> DailyFinanceRead:
    return data.create(daily_finance)

def delete(id: int) -> bool:
    return data.delete(id)