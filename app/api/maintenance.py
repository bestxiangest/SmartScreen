#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 维修工单管理API
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models import MaintenanceOrder, User, Device, beijing_now
from app.extensions import db
from app.helpers.responses import api_success, api_error, api_paginated_success
from datetime import datetime, date, timedelta
from sqlalchemy import or_, and_, func
import json

@api_bp.route('/maintenance-orders', methods=['POST'])
@jwt_required()
def create_maintenance_order():
    """创建维修工单"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['title', 'description', 'priority']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"{field}不能为空", 400)
        
        # 验证优先级
        if data['priority'] not in ['low', 'medium', 'high', 'urgent']:
            return api_error("优先级必须是 low, medium, high, urgent 之一", 400)
        
        # 验证设备是否存在（如果提供了设备ID）
        if data.get('device_id'):
            device = Device.query.get(data['device_id'])
            if not device:
                return api_error("设备不存在", 400)
        
        # 生成工单号
        today = date.today()
        order_number = f"MO{today.strftime('%Y%m%d')}{MaintenanceOrder.query.filter(MaintenanceOrder.created_at >= today).count() + 1:04d}"
        
        # 解析预期完成日期
        expected_completion_date = None
        if data.get('expected_completion_date'):
            try:
                expected_completion_date = datetime.strptime(data['expected_completion_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("预期完成日期格式错误，应为YYYY-MM-DD", 400)
        
        # 创建维修工单
        maintenance_order = MaintenanceOrder(
            order_number=order_number,
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            device_id=data.get('device_id'),
            location=data.get('location'),
            reporter_id=current_user_id,
            expected_completion_date=expected_completion_date,
            attachments=data.get('attachments', [])
        )
        
        db.session.add(maintenance_order)
        db.session.commit()
        
        return api_success(data=maintenance_order.to_dict(), message="维修工单创建成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建维修工单失败: {str(e)}", 500)

@api_bp.route('/maintenance-orders', methods=['GET'])
@jwt_required()
def get_maintenance_orders():
    """获取维修工单列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status')
        priority = request.args.get('priority')
        assignee_id = request.args.get('assignee_id', type=int)
        reporter_id = request.args.get('reporter_id', type=int)
        device_id = request.args.get('device_id', type=int)
        keyword = request.args.get('keyword')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 构建查询
        query = MaintenanceOrder.query
        
        # 按状态筛选
        if status:
            query = query.filter(MaintenanceOrder.status == status)
        
        # 按优先级筛选
        if priority:
            query = query.filter(MaintenanceOrder.priority == priority)
        
        # 按处理人筛选
        if assignee_id:
            query = query.filter(MaintenanceOrder.assignee_id == assignee_id)
        
        # 按报告人筛选
        if reporter_id:
            query = query.filter(MaintenanceOrder.reporter_id == reporter_id)
        
        # 按设备筛选
        if device_id:
            query = query.filter(MaintenanceOrder.device_id == device_id)
        
        # 关键词搜索（标题、描述、位置）
        if keyword:
            query = query.filter(
                or_(
                    MaintenanceOrder.title.like(f'%{keyword}%'),
                    MaintenanceOrder.description.like(f'%{keyword}%'),
                    MaintenanceOrder.location.like(f'%{keyword}%')
                )
            )
        
        # 按日期范围筛选
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(MaintenanceOrder.created_at >= start_dt)
            except ValueError:
                return api_error("开始日期格式错误，应为YYYY-MM-DD", 400)
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                # 包含结束日期的整天
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(MaintenanceOrder.created_at <= end_dt)
            except ValueError:
                return api_error("结束日期格式错误，应为YYYY-MM-DD", 400)
        
        # 按创建时间倒序排序
        query = query.order_by(MaintenanceOrder.created_at.desc())
        
        # 分页查询
        total = query.count()
        orders = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [order.to_dict() for order in orders]
        
        return api_paginated_success(data, page, limit, total, "获取维修工单列表成功")
        
    except Exception as e:
        return api_error(f"获取维修工单列表失败: {str(e)}", 500)

@api_bp.route('/maintenance-orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_maintenance_order_detail(order_id):
    """获取维修工单详情"""
    try:
        order = MaintenanceOrder.query.get(order_id)
        
        if not order:
            return api_error("维修工单不存在", 404)
        
        return api_success(data=order.to_dict(), message="获取维修工单详情成功")
        
    except Exception as e:
        return api_error(f"获取维修工单详情失败: {str(e)}", 500)

@api_bp.route('/maintenance-orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_maintenance_order(order_id):
    """更新维修工单"""
    try:
        order = MaintenanceOrder.query.get(order_id)
        
        if not order:
            return api_error("维修工单不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证优先级
        if 'priority' in data and data['priority'] not in ['low', 'medium', 'high', 'urgent']:
            return api_error("优先级必须是 low, medium, high, urgent 之一", 400)
        
        # 验证状态
        if 'status' in data and data['status'] not in ['pending', 'in_progress', 'completed', 'cancelled']:
            return api_error("状态必须是 pending, in_progress, completed, cancelled 之一", 400)
        
        # 验证设备是否存在（如果提供了设备ID）
        if 'device_id' in data and data['device_id']:
            device = Device.query.get(data['device_id'])
            if not device:
                return api_error("设备不存在", 400)
        
        # 验证处理人是否存在（如果提供了处理人ID）
        if 'assignee_id' in data and data['assignee_id']:
            assignee = User.query.get(data['assignee_id'])
            if not assignee:
                return api_error("处理人不存在", 400)
        
        # 解析预期完成日期
        if 'expected_completion_date' in data and data['expected_completion_date']:
            try:
                data['expected_completion_date'] = datetime.strptime(data['expected_completion_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("预期完成日期格式错误，应为YYYY-MM-DD", 400)
        
        # 解析实际完成日期
        if 'actual_completion_date' in data and data['actual_completion_date']:
            try:
                data['actual_completion_date'] = datetime.strptime(data['actual_completion_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("实际完成日期格式错误，应为YYYY-MM-DD", 400)
        
        # 更新字段
        for field in ['title', 'description', 'priority', 'status', 'device_id', 
                     'location', 'assignee_id', 'expected_completion_date', 
                     'actual_completion_date', 'resolution', 'attachments']:
            if field in data:
                setattr(order, field, data[field])
        
        # 如果状态变为已完成，自动设置完成时间
        if 'status' in data and data['status'] == 'completed' and not order.actual_completion_date:
            order.actual_completion_date = date.today()
        
        db.session.commit()
        
        return api_success(data=order.to_dict(), message="更新维修工单成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新维修工单失败: {str(e)}", 500)

@api_bp.route('/maintenance-orders/<int:order_id>/assign', methods=['PUT'])
@jwt_required()
def assign_maintenance_order(order_id):
    """分配维修工单"""
    try:
        order = MaintenanceOrder.query.get(order_id)
        
        if not order:
            return api_error("维修工单不存在", 404)
        
        data = request.get_json()
        
        if not data or not data.get('assignee_id'):
            return api_error("处理人ID不能为空", 400)
        
        # 验证处理人是否存在
        assignee = User.query.get(data['assignee_id'])
        if not assignee:
            return api_error("处理人不存在", 400)
        
        # 更新分配信息
        order.assignee_id = data['assignee_id']
        order.assigned_at = beijing_now()
        
        # 如果工单状态是待处理，自动更新为处理中
        if order.status == 'pending':
            order.status = 'in_progress'
        
        db.session.commit()
        
        return api_success(data=order.to_dict(), message="维修工单分配成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"分配维修工单失败: {str(e)}", 500)

@api_bp.route('/maintenance-orders/<int:order_id>/complete', methods=['PUT'])
@jwt_required()
def complete_maintenance_order(order_id):
    """完成维修工单"""
    try:
        current_user_id = get_jwt_identity()
        order = MaintenanceOrder.query.get(order_id)
        
        if not order:
            return api_error("维修工单不存在", 404)
        
        # 检查权限：只有分配的处理人可以完成工单
        if order.assignee_id != current_user_id:
            return api_error("只有分配的处理人可以完成工单", 403)
        
        if order.status == 'completed':
            return api_error("工单已完成", 400)
        
        data = request.get_json()
        
        # 更新完成信息
        order.status = 'completed'
        order.actual_completion_date = date.today()
        order.resolution = data.get('resolution', '')
        
        if data.get('attachments'):
            order.attachments = data['attachments']
        
        db.session.commit()
        
        return api_success(data=order.to_dict(), message="维修工单完成成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"完成维修工单失败: {str(e)}", 500)

@api_bp.route('/maintenance-orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_maintenance_order(order_id):
    """删除维修工单"""
    try:
        order = MaintenanceOrder.query.get(order_id)
        
        if not order:
            return api_error("维修工单不存在", 404)
        
        # 只有待处理状态的工单可以删除
        if order.status != 'pending':
            return api_error("只有待处理状态的工单可以删除", 400)
        
        db.session.delete(order)
        db.session.commit()
        
        return api_success(message="删除维修工单成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除维修工单失败: {str(e)}", 500)

@api_bp.route('/maintenance-orders/statistics', methods=['GET'])
@jwt_required()
def get_maintenance_statistics():
    """获取维修工单统计"""
    try:
        period = request.args.get('period', 'month')
        assignee_id = request.args.get('assignee_id', type=int)
        
        # 基础统计
        query = MaintenanceOrder.query
        if assignee_id:
            query = query.filter(MaintenanceOrder.assignee_id == assignee_id)
        
        total_orders = query.count()
        pending_orders = query.filter(MaintenanceOrder.status == 'pending').count()
        in_progress_orders = query.filter(MaintenanceOrder.status == 'in_progress').count()
        completed_orders = query.filter(MaintenanceOrder.status == 'completed').count()
        cancelled_orders = query.filter(MaintenanceOrder.status == 'cancelled').count()
        
        # 优先级分布
        urgent_orders = query.filter(MaintenanceOrder.priority == 'urgent').count()
        high_orders = query.filter(MaintenanceOrder.priority == 'high').count()
        medium_orders = query.filter(MaintenanceOrder.priority == 'medium').count()
        low_orders = query.filter(MaintenanceOrder.priority == 'low').count()
        
        # 时间范围统计
        now = datetime.now()
        if period == 'day':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now.weekday())
        else:  # month
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        period_query = query.filter(MaintenanceOrder.created_at >= start_time)
        period_total = period_query.count()
        period_completed = period_query.filter(MaintenanceOrder.status == 'completed').count()
        
        # 完成率
        completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
        period_completion_rate = (period_completed / period_total * 100) if period_total > 0 else 0
        
        # 平均处理时间（已完成的工单）
        completed_orders_with_dates = query.filter(
            MaintenanceOrder.status == 'completed',
            MaintenanceOrder.actual_completion_date.isnot(None)
        ).all()
        
        if completed_orders_with_dates:
            total_days = sum(
                (order.actual_completion_date - order.created_at.date()).days
                for order in completed_orders_with_dates
            )
            avg_completion_days = total_days / len(completed_orders_with_dates)
        else:
            avg_completion_days = 0
        
        # 处理人工作量统计
        assignee_stats = db.session.query(
            User.id,
            User.full_name,
            func.count(MaintenanceOrder.id).label('total_orders'),
            func.sum(func.case([(MaintenanceOrder.status == 'completed', 1)], else_=0)).label('completed_orders')
        ).join(MaintenanceOrder, User.id == MaintenanceOrder.assignee_id).group_by(
            User.id, User.full_name
        ).all()
        
        assignee_workload = [
            {
                'assignee_id': item.id,
                'assignee_name': item.full_name,
                'total_orders': item.total_orders,
                'completed_orders': item.completed_orders or 0,
                'completion_rate': (item.completed_orders or 0) / item.total_orders * 100 if item.total_orders > 0 else 0
            }
            for item in assignee_stats
        ]
        
        data = {
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'in_progress_orders': in_progress_orders,
            'completed_orders': completed_orders,
            'cancelled_orders': cancelled_orders,
            'urgent_orders': urgent_orders,
            'high_orders': high_orders,
            'medium_orders': medium_orders,
            'low_orders': low_orders,
            f'{period}_total': period_total,
            f'{period}_completed': period_completed,
            'completion_rate': round(completion_rate, 2),
            f'{period}_completion_rate': round(period_completion_rate, 2),
            'avg_completion_days': round(avg_completion_days, 1),
            'assignee_workload': assignee_workload
        }
        
        return api_success(data=data, message="获取维修工单统计成功")
        
    except Exception as e:
        return api_error(f"获取维修工单统计失败: {str(e)}", 500)