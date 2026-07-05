from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import hash_password
import uuid

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: uuid.UUID):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all(self):
        return self.db.query(User).all()

    def create(self, user_data: UserCreate):
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role=user_data.role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, data: dict):
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def deactivate(self, user: User):
        user.is_active = False
        self.db.commit()
        return user