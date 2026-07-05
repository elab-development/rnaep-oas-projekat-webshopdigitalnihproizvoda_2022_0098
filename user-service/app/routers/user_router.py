from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.services.auth_service import decode_token
import uuid

router = APIRouter(prefix="/users", tags=["Users"])

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = UserRepository(db).get_by_id(uuid.UUID(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user=Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_my_profile(update_data: UserUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = UserRepository(db)
    data = {k: v for k, v in update_data.model_dump().items() if v is not None}
    return repo.update(current_user, data)

@router.get("/", response_model=list[UserResponse])
def get_all_users(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return UserRepository(db).get_all()

@router.put("/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(user_id: uuid.UUID, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return repo.deactivate(user)