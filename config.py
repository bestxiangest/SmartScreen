#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 配置文件
"""

import os
from datetime import timedelta

class Config:
    """基础配置类"""
    
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'smartscreen-secret-key-2025')
    
    # 数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'zzn20041031')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'smartscreen')
    MYSQL_CHARSET = os.getenv('MYSQL_CHARSET', 'utf8mb4')
    
    # SQLAlchemy配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string-smartscreen')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    
    # CORS配置
    CORS_ORIGINS = ['*']
    
    # 分页配置
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        # 确保上传目录存在
        upload_folder = app.config.get('UPLOAD_FOLDER')
        if upload_folder:
            os.makedirs(upload_folder, exist_ok=True)

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
    # 开发环境数据库
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'smartscreen')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{MYSQL_DATABASE}?charset={Config.MYSQL_CHARSET}"
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    
    # 生产环境的上传目录
    UPLOAD_FOLDER = '/www/wwwroot/SmartScreen/uploads'
    
    # 生产环境严格的CORS配置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',') if os.environ.get('CORS_ORIGINS') else []
    
    # 安全配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    
    # 测试数据库
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'smartscreen')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{MYSQL_DATABASE}?charset={Config.MYSQL_CHARSET}"
    
    # 测试环境使用较短的JWT过期时间
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# 获取当前配置
def get_config():
    """获取当前环境配置"""
    config_name = os.environ.get('FLASK_CONFIG', 'default')
    return config.get(config_name, config['default'])