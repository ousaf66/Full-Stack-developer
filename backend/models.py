from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    mobile = Column(String(50))
    is_active = Column(Boolean, default=False)
    role = Column(String(50), default="user")
    profile_pic = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    otp_code = Column(String(10))
    expires_at = Column(DateTime)
    used = Column(Boolean, default=False)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(Text)
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)
    user = relationship("User")
