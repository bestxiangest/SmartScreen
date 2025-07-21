#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 设备管理API
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models import Device, DeviceCategory, DeviceUsageLog, User
from app import db
from app.helpers.responses import api_success, api_error, api_paginated_success
from datetime import datetime

# 设备分类相关接口
@api_bp.route('/device-categories', methods=['GET'])
def get_device_categories():
    """获取设备分类列表"""
    try:
        categories = DeviceCategory.query.all()
        data = [category.to_dict() for category in categories]
        
        return api_success(data=data, message="获取设备分类列表成功")
        
    except Exception as e:
        return api_error(f"获取设备分类列表失败: {str(e)}", 500)

@api_bp.route('/device-categories', methods=['POST'])
@jwt_required()
def create_device_category():
    """创建设备分类"""
    try:
        data = request.get_json()
        
        if not data or not data.get('category_name'):
            return api_error("分类名称不能为空", 400)
        
        # 检查分类名称是否已存在
        existing_category = DeviceCategory.query.filter_by(
            category_name=data['category_name']
        ).first()
        
        if existing_category:
            return api_error("分类名称已存在", 400)
        
        category = DeviceCategory(category_name=data['category_name'])
        db.session.add(category)
        db.session.commit()
        
        return api_success(data=category.to_dict(), message="创建设备分类成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建设备分类失败: {str(e)}", 500)

# 设备相关接口
@api_bp.route('/devices', methods=['GET'])
def get_devices():
    """获取设备列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        category_id = request.args.get('category_id', type=int)
        status = request.args.get('status')
        
        # 构建查询
        query = Device.query
        
        # 按分类筛选
        if category_id:
            query = query.filter(Device.category_id == category_id)
        
        # 按状态筛选
        if status:
            query = query.filter(Device.status == status)
        
        # 按设备名称排序
        query = query.order_by(Device.device_name.asc())
        
        # 分页查询
        total = query.count()
        devices = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [device.to_dict() for device in devices]
        
        return api_paginated_success(data, page, limit, total, "获取设备列表成功")
        
    except Exception as e:
        return api_error(f"获取设备列表失败: {str(e)}", 500)

@api_bp.route('/devices', methods=['POST'])
@jwt_required()
def create_device():
    """创建设备"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['device_name', 'category_id']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"{field}不能为空", 400)
        
        # 验证分类是否存在
        category = DeviceCategory.query.get(data['category_id'])
        if not category:
            return api_error("设备分类不存在", 400)
        
        # 验证状态是否有效
        if 'status' in data:
            valid_statuses = ['可用', '使用中', '维修中', '报废']
            if data['status'] not in valid_statuses:
                return api_error(f"无效的设备状态，有效状态: {', '.join(valid_statuses)}", 400)
        
        # 解析购置日期
        purchase_date = None
        if data.get('purchase_date'):
            try:
                purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("购置日期格式错误，应为YYYY-MM-DD", 400)
        
        # 创建新设备
        device = Device(
            device_name=data['device_name'],
            category_id=data['category_id'],
            model=data.get('model'),
            status=data.get('status', '可用'),
            location=data.get('location'),
            image_url=data.get('image_url'),
            purchase_date=purchase_date
        )
        
        db.session.add(device)
        db.session.commit()
        
        return api_success(data=device.to_dict(), message="创建设备成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建设备失败: {str(e)}", 500)

@api_bp.route('/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    """获取单个设备详情"""
    try:
        device = Device.query.get(device_id)
        
        if not device:
            return api_error("设备不存在", 404)
        
        return api_success(data=device.to_dict(), message="获取设备详情成功")
        
    except Exception as e:
        return api_error(f"获取设备详情失败: {str(e)}", 500)

@api_bp.route('/devices/<int:device_id>', methods=['PUT'])
@jwt_required()
def update_device(device_id):
    """更新设备"""
    try:
        device = Device.query.get(device_id)
        
        if not device:
            return api_error("设备不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证分类是否存在（如果提供了分类ID）
        if 'category_id' in data:
            category = DeviceCategory.query.get(data['category_id'])
            if not category:
                return api_error("设备分类不存在", 400)
        
        # 验证状态是否有效（如果提供了状态）
        if 'status' in data:
            valid_statuses = ['可用', '使用中', '维修中', '报废']
            if data['status'] not in valid_statuses:
                return api_error(f"无效的设备状态，有效状态: {', '.join(valid_statuses)}", 400)
        
        # 解析购置日期（如果提供）
        if 'purchase_date' in data and data['purchase_date']:
            try:
                data['purchase_date'] = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("购置日期格式错误，应为YYYY-MM-DD", 400)
        
        # 更新字段
        updatable_fields = ['device_name', 'category_id', 'model', 'status', 
                           'location', 'image_url', 'purchase_date']
        for field in updatable_fields:
            if field in data:
                setattr(device, field, data[field])
        
        db.session.commit()
        
        return api_success(data=device.to_dict(), message="更新设备成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新设备失败: {str(e)}", 500)

@api_bp.route('/devices/<int:device_id>', methods=['DELETE'])
@jwt_required()
def delete_device(device_id):
    """删除设备"""
    try:
        device = Device.query.get(device_id)
        
        if not device:
            return api_error("设备不存在", 404)
        
        db.session.delete(device)
        db.session.commit()
        
        return api_success(message="删除设备成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除设备失败: {str(e)}", 500)

# 设备使用记录相关接口
@api_bp.route('/device-usage-logs', methods=['GET'])
@jwt_required()
def get_device_usage_logs():
    """获取设备使用记录列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        device_id = request.args.get('device_id', type=int)
        user_id = request.args.get('user_id', type=int)
        
        # 构建查询
        query = DeviceUsageLog.query
        
        # 按设备筛选
        if device_id:
            query = query.filter(DeviceUsageLog.device_id == device_id)
        
        # 按用户筛选
        if user_id:
            query = query.filter(DeviceUsageLog.user_id == user_id)
        
        # 按借出时间倒序排列
        query = query.order_by(DeviceUsageLog.checkout_time.desc())
        
        # 分页查询
        total = query.count()
        logs = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [log.to_dict() for log in logs]
        
        return api_paginated_success(data, page, limit, total, "获取设备使用记录列表成功")
        
    except Exception as e:
        return api_error(f"获取设备使用记录列表失败: {str(e)}", 500)

@api_bp.route('/devices/<int:device_id>/checkout', methods=['POST'])
@jwt_required()
def checkout_device(device_id):
    """借出设备"""
    try:
        device = Device.query.get(device_id)
        
        if not device:
            return api_error("设备不存在", 404)
        
        if device.status != '可用':
            return api_error("设备当前不可借出", 400)
        
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        # 创建使用记录
        usage_log = DeviceUsageLog(
            device_id=device_id,
            user_id=current_user_id,
            notes=data.get('notes')
        )
        
        # 更新设备状态
        device.status = '使用中'
        
        db.session.add(usage_log)
        db.session.commit()
        
        return api_success(data=usage_log.to_dict(), message="设备借出成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"设备借出失败: {str(e)}", 500)

@api_bp.route('/device-usage-logs/<int:log_id>/checkin', methods=['PUT'])
@jwt_required()
def checkin_device(log_id):
    """归还设备"""
    try:
        usage_log = DeviceUsageLog.query.get(log_id)
        
        if not usage_log:
            return api_error("使用记录不存在", 404)
        
        if usage_log.checkin_time:
            return api_error("设备已归还", 400)
        
        current_user_id = get_jwt_identity()
        
        # 验证是否为借出用户
        if usage_log.user_id != current_user_id:
            return api_error("只能归还自己借出的设备", 403)
        
        data = request.get_json() or {}
        
        # 更新归还时间和备注
        usage_log.checkin_time = datetime.utcnow()
        if 'notes' in data:
            usage_log.notes = data['notes']
        
        # 更新设备状态
        device = usage_log.device
        device.status = '可用'
        
        db.session.commit()
        
        return api_success(data=usage_log.to_dict(), message="设备归还成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"设备归还失败: {str(e)}", 500)