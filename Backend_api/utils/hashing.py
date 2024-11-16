import bcrypt

def hash_password(password: str) -> str:
    # Hash a password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Ensure hashed_password is not None before verification
    if not hashed_password:
        return False
    # Verify a hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

