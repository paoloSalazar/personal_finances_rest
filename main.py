from fastapi import FastAPI
from web import category

app = FastAPI()

app.include_router(category.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True) 