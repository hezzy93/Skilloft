from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.login_schema import UserLogin, Token
from services.login_services import authenticate_user
from utils.login_utils import create_access_token, verify_token
from database import get_db  # assume get_db provides a database session
from fastapi.security import OAuth2PasswordBearer

login_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/login")

# Login Endpoint
@login_router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer", "message": "Successful login"}

# Dependency to get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)



# Example Protected Route
@login_router.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user.email}