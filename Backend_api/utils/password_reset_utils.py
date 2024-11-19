
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from utils.login_utils import settings  # Use settings from login_utils.py
from utils.hashing import hash_password, verify_password  # Import from hashing.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import User
import logging

logger = logging.getLogger(__name__)
# Load environment variables if needed
load_dotenv()  # Ensure .env variables are loaded

# Create Reset Token
def create_reset_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Verify Reset Token
def verify_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None

# Send Reset Email using SMTP
def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:8000/auth/password-reset?token={token}"

    try:
        # Use a 'with' statement for the SMTP session
        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as smtp:
            smtp.starttls()  # Start TLS encryption
            smtp.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)

            # Create email content
            msg = MIMEMultipart()
            msg['From'] = settings.MAIL_FROM
            msg['To'] = email
            msg['Subject'] = "SKILLOFT Password Reset Request"

            # Enhanced HTML content
            body = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                  <h2 style="color: #333; text-align: center;">Password Reset Request</h2>
                  <p style="font-size: 16px; color: #555;">
                    Hello,
                  </p>
                  <p style="font-size: 16px; color: #555;">
                    We received a request to reset your password for your SKILLOFT account. If you did not make this request, please ignore this email.
                  </p>
                  <p style="font-size: 16px; color: #555;">
                    To reset your password, please click the button below:
                  </p>
                  <div style="text-align: center; margin: 20px;">
                    <a href="{reset_link}" style="text-decoration: none;">
                      <button style="background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px; border: none; border-radius: 5px; cursor: pointer;">
                        Reset Password
                      </button>
                    </a>
                  </div>
                  <p style="font-size: 14px; color: #888; text-align: center;">
                    Or copy and paste the following link into your browser:
                  </p>
                  <p style="font-size: 14px; color: #4CAF50; word-wrap: break-word;">
                    <a href="{reset_link}" style="color: #4CAF50;">{reset_link}</a>
                  </p>
                  <p style="font-size: 14px; color: #888; text-align: center;">
                    Thank you,<br>
                    The SKILLOFT Team
                  </p>
                </div>
              </body>
            </html>
            """
            msg.attach(MIMEText(body, 'html'))

            # Send the email
            smtp.send_message(msg)
            logger.info(f"Password reset email sent to {email}")

    except socket.gaierror as e:
        logger.error(f"Network error when sending email to {email}: {e}")
        raise HTTPException(status_code=503, detail="Unable to send email due to a network issue. Please try again later.")

    except smtplib.SMTPException as e:
        logger.error(f"SMTP error when sending email to {email}: {e}")
        raise HTTPException(status_code=503, detail="Unable to send email due to SMTP issues. Please contact support.")

    except Exception as e:
        logger.error(f"Unexpected error when sending email to {email}: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")