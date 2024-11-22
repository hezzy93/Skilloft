from sqlalchemy.orm import Session
from models import models
from fastapi import HTTPException

# Delete user by ID
def delete_user(db: Session, user_id: str):
    # Query the user to delete
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if db_user:
        # Delete the user
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        # Handle case where user is not found
        raise HTTPException(status_code=404, detail="User not found")
