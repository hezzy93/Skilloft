# from fastapi import APIRouter
# from fastapi import Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session
# from database import SessionLocal, engine, Base, get_db
# from schemas import signup_schema
# from services import signup_service


# signup_router = APIRouter()
# # user_router = APIRouter()


# @signup_router.post('Signup')
# def enroll(user: signup_schema.UserCreate, db: Session = Depends(get_db)):
#     db_user = signup_service.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     created_user = signup_service.create_user(db=db, user=user)
    
#     # Publish the user data to RabbitMQ for the backend to consume
#     user_message = {
#         "email": created_user.email,
#         "first_name": created_user.first_name,
#         "last_name": created_user.last_name
#     }
#     return {"message": "Account created successfully", "user": created_user}



# # Endpoint to GET all users
# @signup_router.get('users')
# def get_users(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
#     users = signup_service.get_users(db, offset=offset, limit=limit)
#     return users