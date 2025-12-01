# 模型配置参数模型
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ModelConfig(Base):
    """模型配置参数模型"""
    __tablename__ = "model_config"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False, comment="配置名称")
    monte_carlo_times = Column(Integer, default=10000, comment="蒙特卡洛模拟次数")
    lstm_hidden_layers = Column(Integer, default=3, comment="LSTM隐藏层数量")
    price_elasticity = Column(Float, default=-0.5, comment="价格弹性系数")
    confidence_level = Column(Float, default=0.95, comment="置信度阈值")
    is_default = Column(Boolean, default=False, comment="是否为默认配置")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    station = relationship("Station", backref="model_configs")
