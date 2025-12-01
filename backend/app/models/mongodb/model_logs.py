# 模型日志模型
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ModelLog(BaseModel):
    """模型日志模型"""
    station_id: int
    model_type: str
    status: str = Field(..., pattern="^(training|success|failed)$")
    parameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, float]] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "station_id": 1,
                "model_type": "LSTM",
                "status": "success",
                "parameters": {
                    "hidden_layers": 3,
                    "epochs": 100,
                    "batch_size": 32
                },
                "metrics": {
                    "mae": 0.045,
                    "rmse": 0.067,
                    "r2": 0.92
                },
                "created_at": "2023-11-27T14:30:00",
                "updated_at": "2023-11-27T14:35:00"
            }
        }
