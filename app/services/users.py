#app/services/users.py

from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate
from app.core.security import hash_password

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
    async def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    async def create_user(self, user: UserCreate):
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user