# 数据库连接配置
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# MySQL数据库连接
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB数据库连接
mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
mongo_db = mongo_client.get_database()


# 依赖项：获取MySQL数据库会话
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 依赖项：获取MongoDB数据库
def get_mongo_db():
    """获取MongoDB数据库"""
    return mongo_db
