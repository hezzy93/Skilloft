import logging
from sqlalchemy.orm import Session
from models.models import User
from utils.password_reset_utils import create_reset_token, verify_reset_token, send_reset_email
from utils.hashing import hash_password, verify_password  # Import the verify_password function
from fastapi import BackgroundTasks

# Initialize logger
logger = logging.getLogger(__name__)

# Function to initiate the password reset process by sending an email
def send_password_reset_email(db: Session, email: str, background_tasks: BackgroundTasks) -> bool:
    # Check if the user with the given email exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Password reset requested for non-existent email: {email}")
        return False  # User not found, cannot send reset email

    # Generate a reset token for the user's email
    token = create_reset_token(email)
    
    # Use BackgroundTasks to send the email in the background
    try:
        background_tasks.add_task(send_reset_email, email, token)
        logger.info(f"Background task added for sending password reset email to: {email}")
    except Exception as e:
        logger.error(f"Failed to add background task for sending email to {email}: {e}")
        return False

    return True

# Function to reset the user's password using the reset token and new password
def reset_password(db: Session, token: str, new_password: str) -> bool:
    # Verify the reset token (this should decode and validate the token)
    email = verify_reset_token(token)
    if not email:
        logger.warning(f"Invalid or expired token used for password reset.")
        return False  # Invalid or expired token

    # Check if the user with the provided email exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Password reset attempted for non-existent email: {email}")
        return False  # User not found, cannot reset password

    # Verify if the new password is the same as the old password
    if verify_password(new_password, user.hashed_password):
        logger.info(f"New password is identical to the current password for user {email}. No update needed.")
        return False  # New password is the same as the old password

    # Hash the new password before saving
    hashed_password = hash_password(new_password)
    user.hashed_password = hashed_password  # Update the user's password

    # Commit the password change to the database
    try:
        db.commit()
        logger.info(f"Password successfully updated for user {email}.")
    except Exception as e:
        logger.error(f"Failed to update password for user {email}: {e}")
        db.rollback()  # Rollback in case of an error
        return False

    return True
