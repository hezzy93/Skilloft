import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.signup import signup_router, user_router
from routers.login_router import login_router
from routers.password_reset_router import password_reset_router
from routers.others_router import others_router
from database import SessionLocal,  engine, Base

# Configure logging at the beginning of main.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with specific domains if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(signup_router, prefix="/signup", tags=["Signup"])
app.include_router(login_router, prefix="/login", tags=["Login"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(password_reset_router, prefix="/auth", tags=["Authentication"])
app.include_router(others_router, prefix="/others", tags=["Users"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
