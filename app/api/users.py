#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 用户管理API
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.api import api_bp
from app.models import User, Role, UserRole
from app.helpers.responses import api_success, api_error, api_paginated_success, format_validation_error

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """获取用户列表"""
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        # 验证分页参数
        if page < 1:
            return api_error("页码必须大于0", 422)
        if limit < 1:
            return api_error("每页数量必须大于0", 422)
        if limit > 100:  # 限制最大每页数量
            return api_error("每页数量不能超过100", 422)
        
        # 获取筛选参数
        role_name = request.args.get('role')
        search = request.args.get('search')  # 搜索用户名或姓名
        
        # 构建查询
        query = User.query
        
        # 按角色筛选
        if role_name:
            query = query.join(UserRole).join(Role).filter(Role.role_name == role_name)
        
        # 搜索功能
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                db.or_(
                    User.username.like(search_pattern),
                    User.full_name.like(search_pattern)
                )
            )
        
        # 排序
        query = query.order_by(User.created_at.desc())
        
        # 分页
        pagination = query.paginate(
            page=page, per_page=limit, error_out=False
        )
        
        users_data = []
        for user in pagination.items:
            user_dict = user.to_dict()
            # 获取用户角色
            roles = db.session.query(Role).join(UserRole).filter(UserRole.user_id == user.id).all()
            user_dict['roles'] = [role.to_dict() for role in roles]
            users_data.append(user_dict)
        
        return api_paginated_success(
            data=users_data,
            page=page,
            limit=limit,
            total=pagination.total,
            message="获取用户列表成功"
        )
        
    except Exception as e:
        return api_error(f"获取用户列表失败: {str(e)}", 500)

@api_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    """创建新用户"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['username', 'password', 'full_name']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"缺少必填字段: {field}", 400)
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username']).first():
            return api_error("用户名已存在", 400)
        
        # 注意：User模型中暂时没有status字段，如需要可以后续添加
        
        # 创建用户
        user = User(
            username=data['username'],
            password_hash=generate_password_hash(data['password'], method='scrypt'),
            full_name=data['full_name'],
            major=data.get('major'),
            class_name=data.get('class'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            avatar_url=data.get('avatar_url')
        )
        
        db.session.add(user)
        db.session.flush()  # 获取用户ID
        
        # 处理角色分配
        role_ids = data.get('role_ids', [])
        if role_ids:
            for role_id in role_ids:
                # 验证角色是否存在
                role = Role.query.get(role_id)
                if not role:
                    return api_error(f"角色ID {role_id} 不存在", 400)
                
                user_role = UserRole(
                    user_id=user.id,
                    role_id=role_id
                )
                db.session.add(user_role)
        
        db.session.commit()
        
        # 返回创建的用户信息
        user_dict = user.to_dict()
        roles = db.session.query(Role).join(UserRole).filter(UserRole.user_id == user.id).all()
        user_dict['roles'] = [role.to_dict() for role in roles]
        
        return api_success(data=user_dict, message="用户创建成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"用户创建失败: {str(e)}", 500)

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """获取单个用户详情"""
    try:
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        user_dict = user.to_dict()
        # 获取用户角色
        roles = db.session.query(Role).join(UserRole).filter(UserRole.user_id == user.id).all()
        user_dict['roles'] = [role.to_dict() for role in roles]
        
        return api_success(data=user_dict, message="获取用户详情成功")
        
    except Exception as e:
        return api_error(f"获取用户详情失败: {str(e)}", 500)

@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """更新用户信息"""
    try:
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        data = request.get_json()
        
        # 检查用户名是否已被其他用户使用
        if 'username' in data and data['username'] != user.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                return api_error("用户名已存在", 400)
        
        # 更新基本信息
        updatable_fields = ['username', 'full_name', 'major', 'email', 'phone_number', 'avatar_url']
        for field in updatable_fields:
            if field in data:
                if field == 'class':
                    setattr(user, 'class_name', data[field])
                else:
                    setattr(user, field, data[field])
        
        # 特殊处理class字段
        if 'class' in data:
            user.class_name = data['class']
        
        # 更新密码（如果提供）
        if 'password' in data and data['password']:
            user.password_hash = generate_password_hash(data['password'], method='scrypt')
        
        # 处理角色更新
        if 'role_ids' in data:
            # 删除现有角色关联
            UserRole.query.filter_by(user_id=user_id).delete()
            
            # 添加新的角色关联
            role_ids = data['role_ids']
            for role_id in role_ids:
                # 验证角色是否存在
                role = Role.query.get(role_id)
                if not role:
                    return api_error(f"角色ID {role_id} 不存在", 400)
                
                user_role = UserRole(
                    user_id=user_id,
                    role_id=role_id
                )
                db.session.add(user_role)
        
        db.session.commit()
        
        # 返回更新后的用户信息
        user_dict = user.to_dict()
        roles = db.session.query(Role).join(UserRole).filter(UserRole.user_id == user.id).all()
        user_dict['roles'] = [role.to_dict() for role in roles]
        
        return api_success(data=user_dict, message="用户信息更新成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"用户信息更新失败: {str(e)}", 500)

@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """删除用户"""
    try:
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 检查是否为当前登录用户
        current_user_id = int(get_jwt_identity())
        if user_id == current_user_id:
            return api_error("不能删除当前登录用户", 400)
        
        # 删除相关的考勤记录
        from app.models import AttendanceLog
        AttendanceLog.query.filter_by(user_id=user_id).delete()
        
        # 删除用户角色关联
        UserRole.query.filter_by(user_id=user_id).delete()
        
        # 删除用户
        db.session.delete(user)
        db.session.commit()
        
        return api_success(message="用户删除成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"用户删除失败: {str(e)}", 500)

@api_bp.route('/users/<int:user_id>/roles', methods=['GET'])
@jwt_required()
def get_user_roles(user_id):
    """获取用户角色"""
    try:
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        roles = db.session.query(Role).join(UserRole).filter(UserRole.user_id == user_id).all()
        roles_data = [role.to_dict() for role in roles]
        
        return api_success(data=roles_data, message="获取用户角色成功")
        
    except Exception as e:
        return api_error(f"获取用户角色失败: {str(e)}", 500)

@api_bp.route('/users/<int:user_id>/roles', methods=['PUT'])
@jwt_required()
def update_user_roles(user_id):
    """更新用户角色"""
    try:
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        data = request.get_json()
        role_ids = data.get('role_ids', [])
        
        # 删除现有角色关联
        UserRole.query.filter_by(user_id=user_id).delete()
        
        # 添加新的角色关联
        for role_id in role_ids:
            # 验证角色是否存在
            role = Role.query.get(role_id)
            if not role:
                return api_error(f"角色ID {role_id} 不存在", 400)
            
            user_role = UserRole(
                user_id=user_id,
                role_id=role_id
            )
            db.session.add(user_role)
        
        db.session.commit()
        
        # 返回更新后的角色列表
        roles = db.session.query(Role).join(UserRole).filter(UserRole.user_id == user_id).all()
        roles_data = [role.to_dict() for role in roles]
        
        return api_success(data=roles_data, message="用户角色更新成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"用户角色更新失败: {str(e)}", 500)

@api_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_roles():
    """获取所有角色"""
    try:
        roles = Role.query.order_by(Role.id).all()
        roles_data = [role.to_dict() for role in roles]
        
        return api_success(data=roles_data, message="获取角色列表成功")
        
    except Exception as e:
        return api_error(f"获取角色列表失败: {str(e)}", 500)

@api_bp.route('/roles', methods=['POST'])
@jwt_required()
def create_role():
    """创建新角色"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('role_name'):
            return api_error("缺少必填字段: role_name", 400)
        
        # 检查角色名是否已存在
        if Role.query.filter_by(role_name=data['role_name']).first():
            return api_error("角色名已存在", 400)
        
        # 创建角色
        role = Role(
            role_name=data['role_name'],
            permissions=data.get('permissions', [])
        )
        
        db.session.add(role)
        db.session.commit()
        
        return api_success(data=role.to_dict(), message="角色创建成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"角色创建失败: {str(e)}", 500)

@api_bp.route('/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
def update_role(role_id):
    """更新角色信息"""
    try:
        role = Role.query.get(role_id)
        if not role:
            return api_error("角色不存在", 404)
        
        data = request.get_json()
        
        # 检查角色名是否已被其他角色使用
        if 'role_name' in data and data['role_name'] != role.role_name:
            existing_role = Role.query.filter_by(role_name=data['role_name']).first()
            if existing_role:
                return api_error("角色名已存在", 400)
        
        # 更新角色信息
        if 'role_name' in data:
            role.role_name = data['role_name']
        if 'permissions' in data:
            role.permissions = data['permissions']
        
        db.session.commit()
        
        return api_success(data=role.to_dict(), message="角色信息更新成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"角色信息更新失败: {str(e)}", 500)

@api_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(role_id):
    """删除角色"""
    try:
        role = Role.query.get(role_id)
        if not role:
            return api_error("角色不存在", 404)
        
        # 检查是否有用户使用此角色
        user_count = UserRole.query.filter_by(role_id=role_id).count()
        if user_count > 0:
            return api_error(f"无法删除角色，还有 {user_count} 个用户使用此角色", 400)
        
        # 删除角色
        db.session.delete(role)
        db.session.commit()
        
        return api_success(message="角色删除成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"角色删除失败: {str(e)}", 500)