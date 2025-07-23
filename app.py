#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 应用入口
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from datetime import timedelta
import os
import hmac
import hashlib

# 修复JWT HMAC digestmod问题
def patch_jwt_hmac():
    """修复Flask-JWT-Extended在某些环境下的HMAC digestmod问题"""
    try:
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

from app.extensions import db, jwt

# 创建Flask应用
app = Flask(__name__)

# 基础配置
app.config['SECRET_KEY'] = 'smartscreen-secret-key-2025'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zzn20041031@localhost:3306/smartscreen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-smartscreen'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_ALGORITHM'] = 'HS256'  # 显式指定JWT算法

# 文件上传配置
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化扩展
db.init_app(app)
jwt.init_app(app)
CORS(app, origins=['*'])

# 注册蓝图
from app.api import api_bp
from app.main import main_bp
app.register_blueprint(api_bp, url_prefix='/api/v1')
app.register_blueprint(main_bp)

# 创建数据库表
with app.app_context():
    from app import models
    db.create_all()

@app.route('/')
def index():
    """主页"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """管理后台主页"""
    return render_template('index.html')

@app.route('/login')
def login():
    """登录页面"""
    return render_template('login.html')

@app.route('/qr-display')
def qr_display_page():
    """二维码显示页面"""
    return render_template('qr_display.html')

@app.route('/checkin')
def checkin_form_page():
    """签到表单页面"""
    return render_template('checkin_form.html')

@app.route('/qr-checkin')
def qr_checkin_page():
    """二维码签到页面（保持兼容性）"""
    return render_template('qr_checkin.html')

@app.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'message': '系统运行正常'
    })

@app.route('/api/v1/test') 
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