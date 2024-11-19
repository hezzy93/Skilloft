from pydantic import BaseModel, EmailStr

# Request schema for initiating password reset
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Confirm password reset with token and new password
class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
