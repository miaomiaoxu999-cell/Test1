# 系统日志模型
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SystemLog(BaseModel):
    """系统日志模型"""
    level: str = Field(..., pattern="^(debug|info|warning|error|critical)$")
    message: str
    module: Optional[str] = None
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "level": "info",
                "message": "系统启动成功",
                "module": "main",
                "created_at": "2023-11-27T14:30:00"
            }
        }
