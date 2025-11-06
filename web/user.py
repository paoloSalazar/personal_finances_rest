import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.schemas.user import User
from service import user as service
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/api/users")

oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")

def unauthed():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Create access token for user"""
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.name}, expires=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Get current user from access token"""
    return {"token": token}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: User) -> User:
    """Create a new user"""
    return service.create(user)

