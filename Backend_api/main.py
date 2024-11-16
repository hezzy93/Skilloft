from fastapi import FastAPI
from routers.signup import signup_router, user_router
from routers.login_router import login_router
from database import SessionLocal,  engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(signup_router, prefix="/signup", tags=["Signup"])
app.include_router(login_router, prefix="/login", tags=["Login"])
app.include_router(user_router, prefix="/user", tags=["User"])
@app.get("/")
def read_root():
    return {"Hello": "World"}
