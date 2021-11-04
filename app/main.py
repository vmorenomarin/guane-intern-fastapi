"""
This script is used to run main functions using FastAPI.

Author: Victor Moreno Marin
Date: 03/11/2021
"""

# Python libraries
from datetime import timedelta

# FastAPI libraries
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# App functions, models and routes
from models.token import Token
from controllers.login import authenticate_user, create_access_token
from routes.dog import dog
from routes.user import user
from routes.upload import upload
from config.db import client

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database instance
db = client["guane_db"]

# FastAPI instance
app = FastAPI(
    title="Guane-Intern-FastAPI",
    description="REST API builded using FastAPI \
              framework and MondoDB as database.",
)


# Authentication
@app.post("/token", response_model=Token, tags=["Login"])
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()
        ):
    """
    Post Token.

    This function returns the token access to use JWT. Raise and
    exception message if user does not exist or type invalid passsword.

    Parameters:
        - form_data: OAuth2PasswordRequestForm ->
        A form to resquest password using OA2.

    Returns a dictionary with access and type token.
    """
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

# Include routes
app.include_router(user)
app.include_router(dog)
app.include_router(upload)
