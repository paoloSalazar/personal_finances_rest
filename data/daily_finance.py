from .init import conn, cursor
from model.schemas.daily_finance import DailyFinanceBase, DailyFinanceCreate, DailyFinanceRead
from model.tables.daily_finance import DailyFinance

cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_finances (
	id INTEGER NOT NULL, 
	date DATE NOT NULL, 
	description VARCHAR(280), 
	amount INTEGER NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	category_id INTEGER NOT NULL, 
	observations VARCHAR(500), 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id)
) 
""")

def row_to_schema(row: tuple) -> DailyFinanceRead:
    """convert a database row to a CategoryRead schema"""
    (id, date, amount, type, category_id, observations, item, payment_method) = row
    return DailyFinanceRead(
        id=id, 
        date=date, 
        amount=amount, 
        type=type, 
        category_id=category_id, 
        observations=observations, 
        item=item, 
        payment_method=payment_method)

def schema_to_dict(daily_finance: DailyFinanceBase) -> dict:
    """convert a DailyFinance schema to a dictionary"""
    return daily_finance.model_dump()

def get_one(id: int) -> DailyFinanceRead | None:
    """return one daily finance by id"""
    qry = "SELECT id,date,amount,type,category_id,observations,item,payment_method FROM daily_finances WHERE id=:id"
    params = {"id": id}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    return row_to_schema(row) if row else None

def get_all() -> list[DailyFinanceRead]:
    """return all daily finances"""
    qry = "SELECT id,date,amount,type,category_id,observations,item,payment_method FROM daily_finances"
    cursor.execute(qry)
    return [row_to_schema(row) for row in cursor.fetchall()]

def create(daily_finance: DailyFinanceCreate) -> DailyFinanceRead:
    qry = """INSERT INTO daily_finances 
             (date, amount, type, category_id, observations, item, payment_method) 
             VALUES 
             (:date, :amount, :type, :category_id, :observations, :item, :payment_method)"""
    params = schema_to_dict(daily_finance)
    cursor.execute(qry, params)
    conn.commit()  
    return get_one(cursor.lastrowid)

def delete(id: int) -> bool:
    qry = "DELETE FROM daily_finances WHERE id=:id"
    params = {"id": id}
    result = cursor.execute(qry, params)
    conn.commit()  
    return result.rowcount > 0
