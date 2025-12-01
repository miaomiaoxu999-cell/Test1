# 预测结果模型
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class PredictResult(Base):
    """预测结果模型"""
    __tablename__ = "predict_result"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=False, index=True)
    time_slot = Column(DateTime(timezone=True), nullable=False, index=True)
    predicted_amount_mean = Column(Float, nullable=False, comment="预测充电量均值(kWh)")
    predicted_amount_lower = Column(Float, nullable=False, comment="预测充电量下限(kWh)")
    predicted_amount_upper = Column(Float, nullable=False, comment="预测充电量上限(kWh)")
    suggested_price_mean = Column(Float, nullable=False, comment="建议价格均值(元/kWh)")
    suggested_price_lower = Column(Float, nullable=False, comment="建议价格下限(元/kWh)")
    suggested_price_upper = Column(Float, nullable=False, comment="建议价格上限(元/kWh)")
    revenue_prediction = Column(Float, nullable=False, comment="收益预测(元)")
    model_config_id = Column(Integer, ForeignKey("model_config.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    station = relationship("Station", backref="predict_results")
    model_config = relationship("ModelConfig", backref="predict_results")
