#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 应用入口
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os

# 创建Flask应用
app = Flask(__name__)

# 基础配置
app.config['SECRET_KEY'] = 'smartscreen-secret-key-2025'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zzn20041031@localhost:3306/smartscreen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

# 初始化扩展
from app import db, jwt
db.init_app(app)
jwt.init_app(app)
CORS(app, origins=['*'])

# 注册API蓝图
from app.api import api_bp
app.register_blueprint(api_bp, url_prefix='/api/v1')

# 创建数据库表
with app.app_context():
    from app import models
    db.create_all()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/login')
def login():
    """登录页面"""
    return render_template('login.html')

@app.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'message': '系统运行正常'
    })

@app.route('/api/test') 
def api_test():
    """API测试接口"""
    return jsonify({
        'success': True,
        'message': 'API测试成功',
        'data': {
            'timestamp': '2024-01-01T12:00:00Z',
            'server': 'Flask Development Server'
        }
    })

if __name__ == '__main__':
    # 从环境变量获取配置
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"智慧实验室电子班牌系统启动中...")
    print(f"访问地址: http://{host}:{port}")
    print(f"调试模式: {'开启' if debug else '关闭'}")
    
    # 启动应用
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )