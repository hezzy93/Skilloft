from sqlalchemy.orm import Session
from models import models
# import schemas
from schemas import signup_schema
from sqlalchemy import func
from fastapi import HTTPException
from utils.hashing import hash_password

# Create User
def create_user(db: Session, user: signup_schema.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        last_name=None,  # Set last_name to None
        first_name=None,  # Set last_name to None
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user    


# Get User by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email.ilike(email)).first()


#Get all users
def get_users(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.User).offset(offset).limit(limit).all()

