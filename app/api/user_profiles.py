#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 用户个人资料API
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.extensions import db
from app.api import api_bp
from app.models import User, UserProfile
from app.helpers.responses import api_success, api_error

@api_bp.route('/user-profiles', methods=['GET'])
@jwt_required()
def get_user_profiles():
    """获取用户个人资料列表"""
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        # 验证分页参数
        if page < 1:
            return api_error("页码必须大于0", 422)
        if limit < 1:
            return api_error("每页数量必须大于0", 422)
        if limit > 100:
            return api_error("每页数量不能超过100", 422)
        
        # 获取搜索参数
        search = request.args.get('search')  # 搜索用户名或姓名
        position = request.args.get('position')  # 按职务筛选
        
        # 构建查询
        query = db.session.query(UserProfile).join(User)
        
        # 搜索功能
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                db.or_(
                    User.username.like(search_pattern),
                    User.full_name.like(search_pattern)
                )
            )
        
        # 按职务筛选
        if position:
            query = query.filter(UserProfile.position.like(f"%{position}%"))
        
        # 排序
        query = query.order_by(User.created_at.desc())
        
        # 分页
        pagination = query.paginate(
            page=page, per_page=limit, error_out=False
        )
        
        profiles_data = []
        for profile in pagination.items:
            profile_dict = profile.to_dict()
            # 添加用户基本信息
            profile_dict['user'] = {
                'id': profile.user.id,
                'username': profile.user.username,
                'full_name': profile.user.full_name,
                'avatar_url': profile.user.avatar_url
            }
            profiles_data.append(profile_dict)
        
        return api_success(
            data={
                'items': profiles_data,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': pagination.total,
                    'total_pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            },
            message="获取用户个人资料列表成功"
        )
        
    except Exception as e:
        return api_error(f"获取用户个人资料列表失败: {str(e)}", 500)

@api_bp.route('/user-profiles/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    """获取指定用户的个人资料"""
    try:
        # 检查用户是否存在
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 获取用户个人资料
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        if not profile:
            return api_error("用户个人资料不存在", 404)
        
        profile_dict = profile.to_dict()
        # 添加用户基本信息
        profile_dict['user'] = {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'major': user.major,
            'class': user.class_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'avatar_url': user.avatar_url,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
        
        return api_success(data=profile_dict, message="获取用户个人资料成功")
        
    except Exception as e:
        return api_error(f"获取用户个人资料失败: {str(e)}", 500)

@api_bp.route('/user-profiles', methods=['POST'])
@jwt_required()
def create_user_profile():
    """创建用户个人资料"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('user_id'):
            return api_error("缺少必填字段: user_id", 400)
        
        user_id = data['user_id']
        
        # 检查用户是否存在
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 检查是否已存在个人资料
        existing_profile = UserProfile.query.filter_by(user_id=user_id).first()
        if existing_profile:
            return api_error("该用户的个人资料已存在", 400)
        
        # 处理出生日期
        birth_date = None
        if data.get('birth_date'):
            try:
                birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("出生日期格式错误，请使用YYYY-MM-DD格式", 400)
        
        # 验证性别
        gender = data.get('gender', '保密')
        if gender not in ['男', '女', '保密']:
            return api_error("性别只能是：男、女、保密", 400)
        
        # 验证技术栈格式
        tech_stack = data.get('tech_stack')
        if tech_stack is not None and not isinstance(tech_stack, list):
            return api_error("技术栈必须是数组格式", 400)
        
        # 创建用户个人资料
        profile = UserProfile(
            user_id=user_id,
            gender=gender,
            birth_date=birth_date,
            position=data.get('position'),
            dormitory=data.get('dormitory'),
            tech_stack=tech_stack
        )
        
        db.session.add(profile)
        db.session.commit()
        
        # 返回创建的个人资料信息
        profile_dict = profile.to_dict()
        profile_dict['user'] = {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'avatar_url': user.avatar_url
        }
        
        return api_success(data=profile_dict, message="用户个人资料创建成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"用户个人资料创建失败: {str(e)}", 500)

@api_bp.route('/user-profiles/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    """更新用户个人资料"""
    try:
        # 检查用户是否存在
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 获取用户个人资料
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return api_error("用户个人资料不存在", 404)
        
        data = request.get_json()
        
        # 更新性别
        if 'gender' in data:
            gender = data['gender']
            if gender not in ['男', '女', '保密']:
                return api_error("性别只能是：男、女、保密", 400)
            profile.gender = gender
        
        # 更新出生日期
        if 'birth_date' in data:
            if data['birth_date']:
                try:
                    profile.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
                except ValueError:
                    return api_error("出生日期格式错误，请使用YYYY-MM-DD格式", 400)
            else:
                profile.birth_date = None
        
        # 更新职务
        if 'position' in data:
            profile.position = data['position']
        
        # 更新宿舍信息
        if 'dormitory' in data:
            profile.dormitory = data['dormitory']
        
        # 更新技术栈
        if 'tech_stack' in data:
            tech_stack = data['tech_stack']
            if tech_stack is not None and not isinstance(tech_stack, list):
                return api_error("技术栈必须是数组格式", 400)
            profile.tech_stack = tech_stack
        
        db.session.commit()
        
        # 返回更新后的个人资料信息
        profile_dict = profile.to_dict()
        profile_dict['user'] = {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'avatar_url': user.avatar_url
        }
        
        return api_success(data=profile_dict, message="用户个人资料更新成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"用户个人资料更新失败: {str(e)}", 500)

@api_bp.route('/user-profiles/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user_profile(user_id):
    """删除用户个人资料"""
    try:
        # 检查用户是否存在
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 获取用户个人资料
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return api_error("用户个人资料不存在", 404)
        
        db.session.delete(profile)
        db.session.commit()
        
        return api_success(message="用户个人资料删除成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"用户个人资料删除失败: {str(e)}", 500)

@api_bp.route('/my-profile', methods=['GET'])
@jwt_required()
def get_my_profile():
    """获取当前登录用户的个人资料"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 获取用户信息
        user = User.query.get(current_user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 获取用户个人资料
        profile = UserProfile.query.filter_by(user_id=current_user_id).first()
        
        if not profile:
            return api_error("用户个人资料不存在", 404)
        
        profile_dict = profile.to_dict()
        # 添加用户基本信息
        profile_dict['user'] = {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'major': user.major,
            'class': user.class_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'avatar_url': user.avatar_url,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
        
        return api_success(data=profile_dict, message="获取个人资料成功")
        
    except Exception as e:
        return api_error(f"获取个人资料失败: {str(e)}", 500)

@api_bp.route('/my-profile', methods=['PUT'])
@jwt_required()
def update_my_profile():
    """更新当前登录用户的个人资料"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 检查用户是否存在
        user = User.query.get(current_user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 获取或创建用户个人资料
        profile = UserProfile.query.filter_by(user_id=current_user_id).first()
        if not profile:
            profile = UserProfile(user_id=current_user_id)
            db.session.add(profile)
        
        data = request.get_json()
        
        # 更新性别
        if 'gender' in data:
            gender = data['gender']
            if gender not in ['男', '女', '保密']:
                return api_error("性别只能是：男、女、保密", 400)
            profile.gender = gender
        
        # 更新出生日期
        if 'birth_date' in data:
            if data['birth_date']:
                try:
                    profile.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
                except ValueError:
                    return api_error("出生日期格式错误，请使用YYYY-MM-DD格式", 400)
            else:
                profile.birth_date = None
        
        # 更新职务
        if 'position' in data:
            profile.position = data['position']
        
        # 更新宿舍信息
        if 'dormitory' in data:
            profile.dormitory = data['dormitory']
        
        # 更新技术栈
        if 'tech_stack' in data:
            tech_stack = data['tech_stack']
            if tech_stack is not None and not isinstance(tech_stack, list):
                return api_error("技术栈必须是数组格式", 400)
            profile.tech_stack = tech_stack
        
        db.session.commit()
        
        # 返回更新后的个人资料信息
        profile_dict = profile.to_dict()
        profile_dict['user'] = {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'major': user.major,
            'class': user.class_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'avatar_url': user.avatar_url,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
        
        return api_success(data=profile_dict, message="个人资料更新成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"个人资料更新失败: {str(e)}", 500)