# 实际回流数据模型
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ActualData(Base):
    """实际回流数据模型"""
    __tablename__ = "actual_data"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=False, index=True)
    time_slot = Column(DateTime(timezone=True), nullable=False, index=True)
    actual_amount = Column(Float, nullable=False, comment="实际充电量(kWh)")
    actual_price = Column(Float, nullable=False, comment="实际定价(元/kWh)")
    user_feedback = Column(Text, comment="用户反馈")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    station = relationship("Station", backref="actual_data")
