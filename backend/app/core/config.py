# 核心配置文件
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""
    # 数据库配置
    DATABASE_URL: str
    MONGODB_URL: str
    
    # FastAPI配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "充电站智能预测平台"
    DEBUG: bool = True
    
    # 模型配置
    DEFAULT_MONTE_CARLO_TIMES: int = 10000
    DEFAULT_LSTM_HIDDEN_LAYERS: int = 3
    DEFAULT_CONFIDENCE_LEVEL: float = 0.95
    
    # JWT配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 日志配置
    LOG_LEVEL: str = "info"
    LOG_FILE: str = "app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建配置实例
settings = Settings()
