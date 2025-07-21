#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 应用包初始化
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
import os

# 初始化扩展
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

def create_app(config_name=None):
    """应用工厂函数"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    
    # 调用配置初始化
    config[config_name].init_app(app)
    
    # 注册蓝图
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # 注册静态文件路由
    from app.main import main_bp
    app.register_blueprint(main_bp)
    
    # 创建数据库表
    with app.app_context():
        from app import models  # 导入所有模型
        db.create_all()
    
    return app