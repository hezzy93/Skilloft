from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from schemas.password_reset_schema import PasswordResetRequest, PasswordResetConfirm
from services.password_reset_services import send_password_reset_email, reset_password

password_reset_router = APIRouter()

# Send Password Reset Email Endpoint
@password_reset_router.post("/password-reset-request")
def password_reset_request(
    data: PasswordResetRequest, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    # Check if user exists before sending the reset email
    user_exists = send_password_reset_email(db, data.email, background_tasks)
    if not user_exists:
        raise HTTPException(
            status_code=404,
            detail="User with the provided email does not exist."
        )
    
    return {"message": "Password reset email sent."}

# Confirm Password Reset Endpoint
@password_reset_router.post("/password-reset-confirm")
def password_reset_confirm(
    data: PasswordResetConfirm, 
    db: Session = Depends(get_db)
):
    # Reset the user's password with the provided token
    if not reset_password(db, data.token, data.new_password):
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token."
        )
    
    return {"message": "Password successfully reset."}
