from fastapi import Header, HTTPException
from jose import jwt, JWTError
from app.config import settings
from typing import Optional

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return {"user_id": payload["sub"], "role": payload["role"], "token": token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")