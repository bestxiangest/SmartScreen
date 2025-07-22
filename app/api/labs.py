#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 实验室信息API
"""

from flask import request
from flask_jwt_extended import jwt_required
from app.api import api_bp
from app.models import Lab
from app.extensions import db
from app.helpers.responses import api_success, api_error
import json

@api_bp.route('/labs', methods=['GET'])
def get_labs():
    """获取实验室信息列表"""
    try:
        labs = Lab.query.all()
        data = [lab.to_dict() for lab in labs]
        
        return api_success(data=data, message="获取实验室信息列表成功")
        
    except Exception as e:
        return api_error(f"获取实验室信息列表失败: {str(e)}", 500)

@api_bp.route('/labs', methods=['POST'])
@jwt_required()
def create_lab():
    """创建实验室信息"""
    try:
        data = request.get_json()
        
        if not data or not data.get('lab_name'):
            return api_error("实验室名称不能为空", 400)
        
        # 检查实验室名称是否已存在
        existing_lab = Lab.query.filter_by(lab_name=data['lab_name']).first()
        if existing_lab:
            return api_error("实验室名称已存在", 400)
        
        # 处理文化理念JSON数据
        culture_info = data.get('culture_info')
        if culture_info and isinstance(culture_info, str):
            try:
                culture_info = json.loads(culture_info)
            except json.JSONDecodeError:
                return api_error("文化理念数据格式错误", 400)
        
        # 创建新实验室
        lab = Lab(
            lab_name=data['lab_name'],
            description=data.get('description'),
            culture_info=culture_info,
            logo_url=data.get('logo_url')
        )
        
        db.session.add(lab)
        db.session.commit()
        
        return api_success(data=lab.to_dict(), message="创建实验室信息成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建实验室信息失败: {str(e)}", 500)

@api_bp.route('/labs/<int:lab_id>', methods=['GET'])
def get_lab(lab_id):
    """获取单个实验室详情"""
    try:
        lab = Lab.query.get(lab_id)
        
        if not lab:
            return api_error("实验室不存在", 404)
        
        return api_success(data=lab.to_dict(), message="获取实验室详情成功")
        
    except Exception as e:
        return api_error(f"获取实验室详情失败: {str(e)}", 500)

@api_bp.route('/labs/<int:lab_id>', methods=['PUT'])
@jwt_required()
def update_lab(lab_id):
    """更新实验室信息"""
    try:
        lab = Lab.query.get(lab_id)
        
        if not lab:
            return api_error("实验室不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 检查实验室名称是否已被其他实验室使用
        if 'lab_name' in data:
            existing_lab = Lab.query.filter(
                Lab.lab_name == data['lab_name'],
                Lab.id != lab_id
            ).first()
            if existing_lab:
                return api_error("实验室名称已存在", 400)
        
        # 处理文化理念JSON数据
        if 'culture_info' in data:
            culture_info = data['culture_info']
            if culture_info and isinstance(culture_info, str):
                try:
                    culture_info = json.loads(culture_info)
                    data['culture_info'] = culture_info
                except json.JSONDecodeError:
                    return api_error("文化理念数据格式错误", 400)
        
        # 更新字段
        updatable_fields = ['lab_name', 'description', 'culture_info', 'logo_url']
        for field in updatable_fields:
            if field in data:
                setattr(lab, field, data[field])
        
        db.session.commit()
        
        return api_success(data=lab.to_dict(), message="更新实验室信息成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新实验室信息失败: {str(e)}", 500)

@api_bp.route('/labs/<int:lab_id>', methods=['DELETE'])
@jwt_required()
def delete_lab(lab_id):
    """删除实验室信息"""
    try:
        lab = Lab.query.get(lab_id)
        
        if not lab:
            return api_error("实验室不存在", 404)
        
        db.session.delete(lab)
        db.session.commit()
        
        return api_success(message="删除实验室信息成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除实验室信息失败: {str(e)}", 500)

@api_bp.route('/v1/labs/default', methods=['GET'])
def get_default_lab():
    """获取默认实验室信息（用于班牌显示）"""
    try:
        # 获取第一个实验室作为默认实验室
        lab = Lab.query.first()
        
        if not lab:
            return api_error("未找到实验室信息", 404)
        
        return api_success(data=lab.to_dict(), message="获取默认实验室信息成功")
        
    except Exception as e:
        return api_error(f"获取默认实验室信息失败: {str(e)}", 500)