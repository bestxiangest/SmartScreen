#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 通知公告API
"""

from flask import request
from flask_jwt_extended import jwt_required
from app.api import api_bp
from app.models import Announcement
from app.extensions import db
from app.helpers.responses import api_success, api_error, api_paginated_success
from datetime import datetime

@api_bp.route('/announcements', methods=['GET'])
def get_announcements():
    """获取通知公告列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        announcement_type = request.args.get('type')
        is_important = request.args.get('is_important')
        
        # 构建查询
        query = Announcement.query
        
        # 按类型筛选
        if announcement_type:
            query = query.filter(Announcement.type == announcement_type)
        
        # 按重要性筛选
        if is_important is not None:
            is_important_bool = is_important.lower() in ['true', '1', 'yes']
            query = query.filter(Announcement.is_important == is_important_bool)
        
        # 按创建时间倒序排列
        query = query.order_by(Announcement.created_at.desc())
        
        # 分页查询
        total = query.count()
        announcements = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [announcement.to_dict() for announcement in announcements]
        
        return api_paginated_success(data, page, limit, total, "获取通知公告列表成功")
        
    except Exception as e:
        return api_error(f"获取通知公告列表失败: {str(e)}", 500)

@api_bp.route('/announcements', methods=['POST'])
@jwt_required()
def create_announcement():
    """创建通知公告"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['title', 'content', 'type']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"{field}不能为空", 400)
        
        # 验证类型是否有效
        valid_types = ['通知', '新闻', '动态', '安全提示', '天气提示', '名言金句']
        if data['type'] not in valid_types:
            return api_error(f"无效的公告类型，有效类型: {', '.join(valid_types)}", 400)
        
        # 创建新公告
        announcement = Announcement(
            title=data['title'],
            content=data['content'],
            author_name=data.get('author_name'),
            type=data['type'],
            is_important=data.get('is_important', False)
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        return api_success(data=announcement.to_dict(), message="创建通知公告成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建通知公告失败: {str(e)}", 500)

@api_bp.route('/announcements/<int:announcement_id>', methods=['GET'])
def get_announcement(announcement_id):
    """获取单个通知公告详情"""
    try:
        announcement = Announcement.query.get(announcement_id)
        
        if not announcement:
            return api_error("通知公告不存在", 404)
        
        return api_success(data=announcement.to_dict(), message="获取通知公告详情成功")
        
    except Exception as e:
        return api_error(f"获取通知公告详情失败: {str(e)}", 500)

@api_bp.route('/announcements/<int:announcement_id>', methods=['PUT'])
@jwt_required()
def update_announcement(announcement_id):
    """更新通知公告"""
    try:
        announcement = Announcement.query.get(announcement_id)
        
        if not announcement:
            return api_error("通知公告不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证类型是否有效（如果提供了类型）
        if 'type' in data:
            valid_types = ['通知', '新闻', '动态', '安全提示', '天气提示', '名言金句']
            if data['type'] not in valid_types:
                return api_error(f"无效的公告类型，有效类型: {', '.join(valid_types)}", 400)
        
        # 更新字段
        updatable_fields = ['title', 'content', 'author_name', 'type', 'is_important']
        for field in updatable_fields:
            if field in data:
                setattr(announcement, field, data[field])
        
        db.session.commit()
        
        return api_success(data=announcement.to_dict(), message="更新通知公告成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新通知公告失败: {str(e)}", 500)

@api_bp.route('/announcements/<int:announcement_id>', methods=['DELETE'])
@jwt_required()
def delete_announcement(announcement_id):
    """删除通知公告"""
    try:
        announcement = Announcement.query.get(announcement_id)
        
        if not announcement:
            return api_error("通知公告不存在", 404)
        
        db.session.delete(announcement)
        db.session.commit()
        
        return api_success(message="删除通知公告成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除通知公告失败: {str(e)}", 500)