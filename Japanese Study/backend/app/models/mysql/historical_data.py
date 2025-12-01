# 历史充电数据模型
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class HistoricalData(Base):
    """历史充电数据模型"""
    __tablename__ = "historical_data"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=False, index=True)
    time_slot = Column(DateTime(timezone=True), nullable=False, index=True)
    charging_amount = Column(Float, nullable=False, comment="充电量(kWh)")
    electricity_price = Column(Float, nullable=False, comment="电价(元/kWh)")
    charging_duration = Column(Float, nullable=False, comment="充电时长(h)")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    station = relationship("Station", backref="historical_data")
