"""
This script is used to authenticate users in the API.

Author: Victor Moreno Marin
Date: 03/11/2021
"""

# Python libraries
from datetime import datetime, timedelta
from typing import Optional

# FastAPI libraries
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# App functions, models and routes
from models.token import UserInDB, TokenData
from models.user import User
from config.db import client

# Secret key generation
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database instance
db = client["guane_db"]

# Hashing password and token validation
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """
    Verify password.

    This function verifies plain pasword and hashed stored password.

    Parameters:
        - plain_password: str -> Plain text password from password form.
        - hashed_password: str -> Hashed password storage in data base.

    Returns True or False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash password.

    This function hashes the plain password using a specified
    encrypting algorithm.

    Parameters:
        - password: str -> Plain password.

    Returns a hashed password.
    """
    return pwd_context.hash(password)


def get_user(db, username: str):
    """
    Get user.

    This function return a user if this exist in database.

    Parameters:
        - db: Database -> Database object.
        - username: str -> User username to locate in database.

    Returns a dictionary with user data, if exist.
    """
    if db.users.find_one({"username": username}):
        user = db.users.find_one({"username": username})
        user_dict = dict(user)
        return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str):
    """
    Authenticate user.

    This function authenticates a user if exists in database
    and password is correct.

    Parameters:
        - db: Database -> Database object.
        - username: str -> User username to locate in database.
        - password: str -> User password to verify.

    Returns a dictionary with authenticated user.
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create access token.

    This function creates a token access that could be expire in specific time.

    Parameters:
        - data: dict -> User data to generete the token.
        - expires_delta: str -> Optional token expiration time.

    Returns a JWT string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get current user.

    This function return the current authenticated user or raise a
    credentials exception header if user is not authenticated.

    Parameters:
        - token: str -> Token that depends on OA2 scheme.

    Returns a dictionary with authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
        ):
    """
    Get current active user.

    Return if a user is active.

    Parameters:
        - current_user: User

    Returns a user dictionary based on User model.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
