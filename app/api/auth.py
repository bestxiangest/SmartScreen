#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 认证API
"""

from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.api import api_bp
from app.models import User
from app.helpers.responses import api_success, api_error
from datetime import timedelta

@api_bp.route('/v1/auth/login', methods=['POST'])
def login():
    """用户登录接口"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return api_error("用户名和密码不能为空", 400)
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return api_error("用户名或密码错误", 401)
        
        # 创建JWT令牌
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=24)
        )
        
        response_data = {
            "token": access_token,
            "user": user.to_dict()
        }
        
        return api_success(data=response_data, message="登录成功")
        
    except Exception as e:
        return api_error(f"登录失败: {str(e)}", 500)

@api_bp.route('/v1/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取当前用户信息"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return api_error("用户不存在", 404)
        
        return api_success(data=user.to_dict(), message="获取用户信息成功")
        
    except Exception as e:
        return api_error(f"获取用户信息失败: {str(e)}", 500)

@api_bp.route('/v1/auth/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    """刷新JWT令牌"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 创建新的访问令牌
        new_token = create_access_token(
            identity=str(current_user_id),
            expires_delta=timedelta(hours=24)
        )
        
        return api_success(data={"token": new_token}, message="令牌刷新成功")
        
    except Exception as e:
        return api_error(f"令牌刷新失败: {str(e)}", 500)