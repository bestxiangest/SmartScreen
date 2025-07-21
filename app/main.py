#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 主蓝图
"""

import os
from flask import Blueprint, send_from_directory, current_app, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """主页"""
    return jsonify({
        'message': '智慧实验室电子班牌系统 API',
        'version': '1.0.0',
        'status': 'running',
        'api_prefix': '/api/v1'
    })

@main_bp.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'message': '系统运行正常'
    })

@main_bp.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """提供上传文件的访问"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        return send_from_directory(upload_folder, filename)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'文件不存在: {str(e)}'
        }), 404

@main_bp.route('/favicon.ico')
def favicon():
    """网站图标"""
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )