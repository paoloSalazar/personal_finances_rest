import logging
from fastapi import FastAPI
from web import category, daily_finance, user

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
app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn
    import ssl
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('ssl/cert.pem', 'ssl/key.pem')
    # uvicorn.run("main:app", host="0.0.0.0", port=443, reload=True, ssl=ssl_context)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,  # Your preferred port
        ssl_keyfile="ssl/key.pem",
        ssl_certfile="ssl/cert.pem"
    )