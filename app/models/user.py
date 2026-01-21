from sqlalchemy import Boolean, Column, Integer, String,ForeignKey
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    name = Column(String, index=True, nullable=True)

 

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    jti = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_revoked = Column(Boolean, default=False)
