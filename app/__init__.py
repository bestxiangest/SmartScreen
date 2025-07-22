#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 应用包初始化
"""

from flask import Flask
from flask_cors import CORS
from config import config
from app.extensions import db, jwt
import os

# 修复JWT HMAC digestmod问题
def patch_jwt_hmac():
    """修复Flask-JWT-Extended在某些环境下的HMAC digestmod问题"""
    try:
        import hmac
        import hashlib
        
        # 保存原始的hmac.new函数
        original_hmac_new = hmac.new
        
        def patched_hmac_new(key, msg=None, digestmod=None):
            """确保HMAC调用时总是包含digestmod参数"""
            if digestmod is None:
                digestmod = hashlib.sha256
            return original_hmac_new(key, msg, digestmod)
        
        # 替换hmac.new函数
        hmac.new = patched_hmac_new
        
    except Exception:
        # 如果补丁失败，静默忽略，让应用继续运行
        pass

# 在导入JWT相关模块之前应用补丁
patch_jwt_hmac()

# 初始化扩展
cors = CORS()

def create_app(config_name=None):
    """应用工厂函数"""
    
    # 获取项目根目录
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
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