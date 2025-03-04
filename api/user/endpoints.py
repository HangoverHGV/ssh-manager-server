"""
This file contains the user endpoints for the API. It includes the following routes:
- GET /: Get all users
- GET /{user_id}: Get a user by ID
- POST /: Create a user
- PUT /{user_id}: Edit a user by ID
- DELETE /{user_id}: Delete a user by ID
- POST /superuser/: Create a superuser
- POST /token: Get an access token
- GET /me: Get the current user (not implemented yet)
"""
from fastapi import (APIRouter, Depends, HTTPException, status)
from configs import get_db, SessionLocal, ACCESS_TOKEN_EXPIRE_DAYS
from fastapi.security import OAuth2PasswordRequestForm
from user.models import User
from user.schema import UserCreate, UserEdit, SuperUserCreate
from user.config import *
from datetime import timedelta
from user.dependencies import authenticate_user, create_access_token, get_current_user


router = APIRouter()


### Routes
@router.get("/", tags=["user"], status_code=status.HTTP_200_OK, responses=USER_GET_ALL_RESPONSE_CONFIG)
async def get_all_users(db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
        for user in users
    ]


@router.get("/{user_id}", tags=["user"], status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }


@router.post("/", tags=["user"], status_code=status.HTTP_201_CREATED, responses=USER_POST_RESPONSE_CONFIG)
async def create_user(user: UserCreate,
                      db: SessionLocal = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = User(name=user.name, email=user.email, is_active=True, is_superuser=False)
    new_user.hash_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        'id': new_user.id,
        'name': new_user.name,
        'email': new_user.email,
        'is_active': new_user.is_active,
        'is_superuser': new_user.is_superuser,
        'created_at': new_user.created_at,
        'updated_at': new_user.updated_at
    }


@router.get("/my/user", tags=["user"], status_code=status.HTTP_200_OK, responses=USER_MY_USER_RESPONSE_CONFIG)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'is_active': current_user.is_active,
        'is_superuser': current_user.is_superuser,
        'created_at': current_user.created_at,
        'updated_at': current_user.updated_at
    }


@router.put("/{user_id}", tags=["user"], status_code=status.HTTP_200_OK, responses=USER_EDIT_RESPONSE_CONFIG)
def edit_user(user_id: int, user: UserEdit, db: SessionLocal = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not current_user.is_superuser and current_user.id != db_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You don't have permission to edit this user")

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    user_response = {
        'id': db_user.id,
        'name': db_user.name,
        'email': db_user.email,
        'is_active': db_user.is_active,
        'is_superuser': db_user.is_superuser,
        'created_at': db_user.created_at,
        'updated_at': db_user.updated_at
    }

    return user_response


@router.delete("/{user_id}", tags=["user"], status_code=status.HTTP_200_OK, responses=USER_DELETE_RESPONSE_CONFIG)
async def delete_user(user_id: int, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not current_user.is_superuser and current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You don't have permission to delete this user")

    db.delete(user)
    db.commit()

    return {"detail": "User deleted successfully"}


@router.post("/superuser", tags=["user"], status_code=status.HTTP_201_CREATED, responses=USER_POST_RESPONSE_CONFIG)
async def create_superuser(user: SuperUserCreate, db: SessionLocal = Depends(get_db)):
    if user.secret_token != SUPERUSER_SECRET_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret token")

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = User(name=user.name, email=user.email, is_active=True, is_superuser=True)
    new_user.hash_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        'id': new_user.id,
        'name': new_user.name,
        'email': new_user.email,
        'is_active': new_user.is_active,
        'is_superuser': new_user.is_superuser,
        'created_at': new_user.created_at,
        'updated_at': new_user.updated_at
    }


@router.post("/token", tags=["user"], status_code=status.HTTP_200_OK, responses=TOKEN_RESPONSE)
async def login_for_access_token(db: SessionLocal = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = authenticate_user(form_data.username, form_data.password, db)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user_db.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/config", tags=["user"], status_code=status.HTTP_200_OK)
async def get_config(db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/config", tags=["user"], status_code=status.HTTP_200_OK)
async def post_config(db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

