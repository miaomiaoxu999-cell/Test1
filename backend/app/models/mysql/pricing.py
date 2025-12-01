# 定价策略模型
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class PricingStrategy(Base):
    """定价策略模型"""
    __tablename__ = "pricing_strategy"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False, comment="策略名称")
    description = Column(Text, comment="策略描述")
    is_active = Column(Boolean, default=False, comment="是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    station = relationship("Station", backref="pricing_strategies")
    time_slot_pricing = relationship("TimeSlotPricing", back_populates="strategy", cascade="all, delete-orphan")


class TimeSlotPricing(Base):
    """时段定价模型"""
    __tablename__ = "time_slot_pricing"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    strategy_id = Column(Integer, ForeignKey("pricing_strategy.id", ondelete="CASCADE"), nullable=False, index=True)
    time_slot = Column(String(20), nullable=False, comment="时段(如:00:00-01:00)")
    price = Column(Float, nullable=False, comment="定价(元/kWh)")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    strategy = relationship("PricingStrategy", back_populates="time_slot_pricing")
