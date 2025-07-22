#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 课程表API
"""

from flask import request
from flask_jwt_extended import jwt_required
from app.api import api_bp
from app.models import Schedule
from app.extensions import db
from app.helpers.responses import api_success, api_error, api_paginated_success
from datetime import datetime, time

@api_bp.route('/schedules', methods=['GET'])
def get_schedules():
    """获取课程表列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        class_date = request.args.get('class_date')
        
        # 构建查询
        query = Schedule.query
        
        # 按上课日期筛选
        if class_date:
            try:
                date_obj = datetime.strptime(class_date, '%Y-%m-%d').date()
                query = query.filter(Schedule.class_date == date_obj)
            except ValueError:
                return api_error("日期格式错误，应为YYYY-MM-DD", 400)
        
        # 按上课日期和开始时间排序
        query = query.order_by(Schedule.class_date.asc(), Schedule.start_time.asc())
        
        # 分页查询
        total = query.count()
        schedules = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [schedule.to_dict() for schedule in schedules]
        
        return api_paginated_success(data, page, limit, total, "获取课程表列表成功")
        
    except Exception as e:
        return api_error(f"获取课程表列表失败: {str(e)}", 500)

@api_bp.route('/schedules', methods=['POST'])
@jwt_required()
def create_schedule():
    """创建课程安排"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['course_name', 'class_date', 'start_time', 'end_time']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"{field}不能为空", 400)
        
        # 解析日期和时间
        try:
            class_date = datetime.strptime(data['class_date'], '%Y-%m-%d').date()
        except ValueError:
            return api_error("上课日期格式错误，应为YYYY-MM-DD", 400)
        
        try:
            start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        except ValueError:
            return api_error("开始时间格式错误，应为HH:MM", 400)
        
        try:
            end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        except ValueError:
            return api_error("结束时间格式错误，应为HH:MM", 400)
        
        # 验证时间逻辑
        if start_time >= end_time:
            return api_error("开始时间必须早于结束时间", 400)
        
        # 检查时间冲突
        existing_schedule = Schedule.query.filter(
            Schedule.class_date == class_date,
            Schedule.start_time < end_time,
            Schedule.end_time > start_time
        ).first()
        
        if existing_schedule:
            return api_error("该时间段已有课程安排", 400)
        
        # 创建新课程安排
        schedule = Schedule(
            course_name=data['course_name'],
            teacher_name=data.get('teacher_name'),
            class_date=class_date,
            start_time=start_time,
            end_time=end_time,
            location=data.get('location')
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        return api_success(data=schedule.to_dict(), message="创建课程安排成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建课程安排失败: {str(e)}", 500)

@api_bp.route('/schedules/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    """获取单个课程安排详情"""
    try:
        schedule = Schedule.query.get(schedule_id)
        
        if not schedule:
            return api_error("课程安排不存在", 404)
        
        return api_success(data=schedule.to_dict(), message="获取课程安排详情成功")
        
    except Exception as e:
        return api_error(f"获取课程安排详情失败: {str(e)}", 500)

@api_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
@jwt_required()
def update_schedule(schedule_id):
    """更新课程安排"""
    try:
        schedule = Schedule.query.get(schedule_id)
        
        if not schedule:
            return api_error("课程安排不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 解析日期和时间（如果提供）
        class_date = schedule.class_date
        start_time = schedule.start_time
        end_time = schedule.end_time
        
        if 'class_date' in data:
            try:
                class_date = datetime.strptime(data['class_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("上课日期格式错误，应为YYYY-MM-DD", 400)
        
        if 'start_time' in data:
            try:
                start_time = datetime.strptime(data['start_time'], '%H:%M').time()
            except ValueError:
                return api_error("开始时间格式错误，应为HH:MM", 400)
        
        if 'end_time' in data:
            try:
                end_time = datetime.strptime(data['end_time'], '%H:%M').time()
            except ValueError:
                return api_error("结束时间格式错误，应为HH:MM", 400)
        
        # 验证时间逻辑
        if start_time >= end_time:
            return api_error("开始时间必须早于结束时间", 400)
        
        # 检查时间冲突（排除当前记录）
        existing_schedule = Schedule.query.filter(
            Schedule.id != schedule_id,
            Schedule.class_date == class_date,
            Schedule.start_time < end_time,
            Schedule.end_time > start_time
        ).first()
        
        if existing_schedule:
            return api_error("该时间段已有课程安排", 400)
        
        # 更新字段
        updatable_fields = ['course_name', 'teacher_name', 'location']
        for field in updatable_fields:
            if field in data:
                setattr(schedule, field, data[field])
        
        # 更新日期和时间
        schedule.class_date = class_date
        schedule.start_time = start_time
        schedule.end_time = end_time
        
        db.session.commit()
        
        return api_success(data=schedule.to_dict(), message="更新课程安排成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新课程安排失败: {str(e)}", 500)

@api_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
def delete_schedule(schedule_id):
    """删除课程安排"""
    try:
        schedule = Schedule.query.get(schedule_id)
        
        if not schedule:
            return api_error("课程安排不存在", 404)
        
        db.session.delete(schedule)
        db.session.commit()
        
        return api_success(message="删除课程安排成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除课程安排失败: {str(e)}", 500)

@api_bp.route('/schedules/today', methods=['GET'])
def get_today_schedules():
    """获取今日课程安排"""
    try:
        today = datetime.now().date()
        
        schedules = Schedule.query.filter(
            Schedule.class_date == today
        ).order_by(Schedule.start_time.asc()).all()
        
        data = [schedule.to_dict() for schedule in schedules]
        
        return api_success(data=data, message="获取今日课程安排成功")
        
    except Exception as e:
        return api_error(f"获取今日课程安排失败: {str(e)}", 500)