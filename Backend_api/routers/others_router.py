from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.others_services import delete_user  # Import the delete function from the service layer
from schemas import signup_schema
from routers.login_router import get_current_user

others_router = APIRouter()

@others_router.delete("/{user_id}", response_model=dict, tags=["Users"])
def delete_user_route(user_id: str, user:signup_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Call the service function to delete the user
    return delete_user(db, user_id)
