from datetime import timedelta


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from models.token import Token
from controllers.login import authenticate_user, create_access_token
from routes.dog import dog
from routes.user import user

from config.db import client



SECRET_KEY = "affc437ef7726471bdb0064c20f0ece5c5ced9667c183db45417447871db5f2e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

db = client["guane_db"]

app = FastAPI(title="Guane-Intern-FastAPI",
              description="REST API builded using FastAPI framework and MondoDB as database."
              )

@app.post("/token", response_model=Token, tags=["Login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(user)
app.include_router(dog)
