# 用户配置模型
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class UserConfig(BaseModel):
    """用户配置模型"""
    user_id: int
    name: str
    config_data: Dict[str, Any]
    is_default: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "name": "默认配置",
                "config_data": {
                    "monte_carlo_times": 10000,
                    "lstm_hidden_layers": 3,
                    "price_elasticity": -0.5,
                    "confidence_level": 0.95
                },
                "is_default": True,
                "created_at": "2023-11-27T14:30:00",
                "updated_at": "2023-11-27T14:30:00"
            }
        }
