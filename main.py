from fastapi import FastAPI
from web import category, daily_finance

app = FastAPI()

app.include_router(category.router)
app.include_router(daily_finance.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True) 