# 充电站模型
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Station(Base):
    """充电站模型"""
    __tablename__ = "stations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    total_piles = Column(Integer, nullable=False)
    capacity = Column(Float, nullable=False)
    cost_per_kwh = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
