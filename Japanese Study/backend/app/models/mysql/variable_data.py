# 变量数据模型
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class VariableData(Base):
    """变量数据模型"""
    __tablename__ = "variable_data"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=False, index=True)
    time_slot = Column(DateTime(timezone=True), nullable=False, index=True)
    temperature = Column(Float, comment="温度(℃)")
    humidity = Column(Float, comment="湿度(%)")
    traffic_flow = Column(Integer, comment="车流量(辆)")
    competitor_price = Column(Float, comment="竞品价格(元/kWh)")
    user_behavior_score = Column(Float, comment="用户行为评分")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    station = relationship("Station", backref="variable_data")
