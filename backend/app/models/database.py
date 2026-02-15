from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    alerts = relationship("Alert", back_populates="user")
    favorites = relationship("FavoriteIndicator", back_populates="user")


class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    unit = Column(String)
    description = Column(Text)
    update_frequency = Column(String)
    data_source = Column(String, default="akshare")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class IndicatorData(Base):
    __tablename__ = "indicator_data"

    id = Column(Integer, primary_key=True, index=True)
    indicator_code = Column(String, ForeignKey("indicators.code"), index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    indicator_code = Column(String, nullable=False)
    condition = Column(String, nullable=False)
    threshold = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="alerts")


class FavoriteIndicator(Base):
    __tablename__ = "favorite_indicators"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    indicator_code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
