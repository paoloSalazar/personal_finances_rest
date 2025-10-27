import logging
from fastapi import FastAPI
from web import category, daily_finance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('app.log')  # Log to file
    ]
)

app = FastAPI()

app.include_router(category.router)
app.include_router(daily_finance.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True) 