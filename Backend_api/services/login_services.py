from sqlalchemy.orm import Session
from models.models import User  # assuming User model is in models.py
from utils.hashing import verify_password  # A utility function for verifying hashed passwords
from fastapi import HTTPException, status

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None






