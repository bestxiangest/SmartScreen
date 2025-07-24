#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 文件上传API
"""

import os
import uuid
from flask import request, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from app.api import api_bp
from app.helpers.responses import api_success, api_error

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(filename):
    """生成唯一的文件名"""
    # 获取文件扩展名
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    # 生成UUID作为文件名
    unique_name = str(uuid.uuid4())
    # 确保图片文件始终有扩展名，如果没有扩展名则默认为jpg
    if not ext:
        ext = 'jpg'  # 默认扩展名
    return f"{unique_name}.{ext}"

@api_bp.route('/upload/image', methods=['POST'])
@jwt_required()
def upload_image():
    """上传图片文件"""
    try:
        # 检查是否有文件在请求中
        if 'file' not in request.files:
            return api_error("没有选择文件", 400)
        
        file = request.files['file']
        
        # 检查文件名是否为空
        if file.filename == '':
            return api_error("没有选择文件", 400)
        
        # 检查文件类型
        if not allowed_file(file.filename):
            allowed_exts = ', '.join(current_app.config['ALLOWED_EXTENSIONS'])
            return api_error(f"不支持的文件类型，支持的类型: {allowed_exts}", 400)
        
        # 检查文件大小
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # 重置文件指针
        
        max_size = current_app.config['MAX_CONTENT_LENGTH']
        if file_size > max_size:
            max_size_mb = max_size / (1024 * 1024)
            return api_error(f"文件大小超过限制，最大允许 {max_size_mb:.1f}MB", 400)
        
        # 生成安全的文件名
        original_filename = secure_filename(file.filename)
        # 如果secure_filename处理后丢失了扩展名，使用原始文件名获取扩展名
        if '.' not in original_filename and '.' in file.filename:
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = generate_unique_filename(f"temp.{ext}")
        else:
            unique_filename = generate_unique_filename(original_filename)
        
        # 确保上传目录存在
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # 保存文件
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # 生成文件URL
        # 这里假设有一个静态文件服务，实际部署时需要配置
        file_url = f"/static/uploads/{unique_filename}"
        
        response_data = {
            'filename': unique_filename,
            'original_filename': original_filename,
            'file_url': file_url,
            'file_size': file_size
        }
        
        return api_success(data=response_data, message="文件上传成功", code=201)
        
    except Exception as e:
        return api_error(f"文件上传失败: {str(e)}", 500)

@api_bp.route('/upload/multiple', methods=['POST'])
@jwt_required()
def upload_multiple_images():
    """批量上传图片文件"""
    try:
        # 检查是否有文件在请求中
        if 'files' not in request.files:
            return api_error("没有选择文件", 400)
        
        files = request.files.getlist('files')
        
        if not files or len(files) == 0:
            return api_error("没有选择文件", 400)
        
        # 限制批量上传的文件数量
        max_files = 10
        if len(files) > max_files:
            return api_error(f"一次最多上传{max_files}个文件", 400)
        
        uploaded_files = []
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # 确保上传目录存在
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        for file in files:
            # 检查文件名是否为空
            if file.filename == '':
                continue
            
            # 检查文件类型
            if not allowed_file(file.filename):
                continue
            
            # 检查文件大小
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # 重置文件指针
            
            max_size = current_app.config['MAX_CONTENT_LENGTH']
            if file_size > max_size:
                continue
            
            # 生成安全的文件名
            original_filename = secure_filename(file.filename)
            # 如果secure_filename处理后丢失了扩展名，使用原始文件名获取扩展名
            if '.' not in original_filename and '.' in file.filename:
                ext = file.filename.rsplit('.', 1)[1].lower()
                unique_filename = generate_unique_filename(f"temp.{ext}")
            else:
                unique_filename = generate_unique_filename(original_filename)
            
            # 保存文件
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            # 生成文件URL
            file_url = f"/static/uploads/{unique_filename}"
            
            uploaded_files.append({
                'filename': unique_filename,
                'original_filename': original_filename,
                'file_url': file_url,
                'file_size': file_size
            })
        
        if not uploaded_files:
            return api_error("没有成功上传任何文件", 400)
        
        response_data = {
            'uploaded_count': len(uploaded_files),
            'files': uploaded_files
        }
        
        return api_success(data=response_data, message=f"成功上传{len(uploaded_files)}个文件", code=201)
        
    except Exception as e:
        return api_error(f"批量文件上传失败: {str(e)}", 500)

@api_bp.route('/upload/info', methods=['GET'])
def get_upload_info():
    """获取上传配置信息"""
    try:
        max_size = current_app.config['MAX_CONTENT_LENGTH']
        max_size_mb = max_size / (1024 * 1024)
        
        upload_info = {
            'max_file_size': max_size,
            'max_file_size_mb': round(max_size_mb, 1),
            'allowed_extensions': list(current_app.config['ALLOWED_EXTENSIONS']),
            'upload_folder': current_app.config['UPLOAD_FOLDER']
        }
        
        return api_success(data=upload_info, message="获取上传配置信息成功")
        
    except Exception as e:
        return api_error(f"获取上传配置信息失败: {str(e)}", 500)