#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 安全须知API
"""

from flask import request
from flask_jwt_extended import jwt_required
from app.api import api_bp
from app.models import SafetyGuideline
from app import db
from app.helpers.responses import api_success, api_error, api_paginated_success

@api_bp.route('/safety-guidelines', methods=['GET'])
def get_safety_guidelines():
    """获取安全须知列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        category = request.args.get('category')
        
        # 构建查询
        query = SafetyGuideline.query
        
        # 按类别筛选
        if category:
            query = query.filter(SafetyGuideline.category == category)
        
        # 按ID排序
        query = query.order_by(SafetyGuideline.id.asc())
        
        # 分页查询
        total = query.count()
        guidelines = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [guideline.to_dict() for guideline in guidelines]
        
        return api_paginated_success(data, page, limit, total, "获取安全须知列表成功")
        
    except Exception as e:
        return api_error(f"获取安全须知列表失败: {str(e)}", 500)

@api_bp.route('/safety-guidelines', methods=['POST'])
@jwt_required()
def create_safety_guideline():
    """创建安全须知"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['category', 'title', 'content']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"{field}不能为空", 400)
        
        # 创建新安全须知
        guideline = SafetyGuideline(
            category=data['category'],
            title=data['title'],
            content=data['content'],
            version=data.get('version')
        )
        
        db.session.add(guideline)
        db.session.commit()
        
        return api_success(data=guideline.to_dict(), message="创建安全须知成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建安全须知失败: {str(e)}", 500)

@api_bp.route('/safety-guidelines/<int:guideline_id>', methods=['GET'])
def get_safety_guideline(guideline_id):
    """获取单个安全须知详情"""
    try:
        guideline = SafetyGuideline.query.get(guideline_id)
        
        if not guideline:
            return api_error("安全须知不存在", 404)
        
        return api_success(data=guideline.to_dict(), message="获取安全须知详情成功")
        
    except Exception as e:
        return api_error(f"获取安全须知详情失败: {str(e)}", 500)

@api_bp.route('/safety-guidelines/<int:guideline_id>', methods=['PUT'])
@jwt_required()
def update_safety_guideline(guideline_id):
    """更新安全须知"""
    try:
        guideline = SafetyGuideline.query.get(guideline_id)
        
        if not guideline:
            return api_error("安全须知不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 更新字段
        updatable_fields = ['category', 'title', 'content', 'version']
        for field in updatable_fields:
            if field in data:
                setattr(guideline, field, data[field])
        
        db.session.commit()
        
        return api_success(data=guideline.to_dict(), message="更新安全须知成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新安全须知失败: {str(e)}", 500)

@api_bp.route('/safety-guidelines/<int:guideline_id>', methods=['DELETE'])
@jwt_required()
def delete_safety_guideline(guideline_id):
    """删除安全须知"""
    try:
        guideline = SafetyGuideline.query.get(guideline_id)
        
        if not guideline:
            return api_error("安全须知不存在", 404)
        
        db.session.delete(guideline)
        db.session.commit()
        
        return api_success(message="删除安全须知成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除安全须知失败: {str(e)}", 500)

@api_bp.route('/safety-guidelines/categories', methods=['GET'])
def get_safety_categories():
    """获取安全须知类别列表"""
    try:
        # 查询所有不重复的类别
        categories = db.session.query(SafetyGuideline.category).distinct().all()
        data = [category[0] for category in categories if category[0]]
        
        return api_success(data=data, message="获取安全须知类别列表成功")
        
    except Exception as e:
        return api_error(f"获取安全须知类别列表失败: {str(e)}", 500)