#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 值班调度管理API
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models import DutySchedule, User, beijing_now
from app.extensions import db
from app.helpers.responses import api_success, api_error, api_paginated_success
from datetime import datetime, date, timedelta
from sqlalchemy import or_, and_, func
import json

@api_bp.route('/duty-schedules', methods=['POST'])
@jwt_required()
def create_duty_schedule():
    """创建值班安排"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['user_id', 'duty_date', 'shift_type']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"{field}不能为空", 400)
        
        # 验证用户是否存在
        user = User.query.get(data['user_id'])
        if not user:
            return api_error("用户不存在", 400)
        
        # 验证班次类型
        if data['shift_type'] not in ['morning', 'afternoon', 'evening', 'night', 'full_day']:
            return api_error("班次类型必须是 morning, afternoon, evening, night, full_day 之一", 400)
        
        # 解析值班日期
        try:
            duty_date = datetime.strptime(data['duty_date'], '%Y-%m-%d').date()
        except ValueError:
            return api_error("值班日期格式错误，应为YYYY-MM-DD", 400)
        
        # 检查是否已有相同用户在同一天同一班次的值班安排
        existing_schedule = DutySchedule.query.filter_by(
            user_id=data['user_id'],
            duty_date=duty_date,
            shift_type=data['shift_type']
        ).first()
        
        if existing_schedule:
            return api_error("该用户在此日期此班次已有值班安排", 400)
        
        # 创建值班安排
        duty_schedule = DutySchedule(
            user_id=data['user_id'],
            duty_date=duty_date,
            shift_type=data['shift_type'],
            location=data.get('location'),
            notes=data.get('notes')
        )
        
        db.session.add(duty_schedule)
        db.session.commit()
        
        return api_success(data=duty_schedule.to_dict(), message="值班安排创建成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建值班安排失败: {str(e)}", 500)

@api_bp.route('/duty-schedules', methods=['GET'])
@jwt_required()
def get_duty_schedules():
    """获取值班安排列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        user_id = request.args.get('user_id', type=int)
        shift_type = request.args.get('shift_type')
        status = request.args.get('status')
        location = request.args.get('location')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 构建查询
        query = DutySchedule.query
        
        # 按用户筛选
        if user_id:
            query = query.filter(DutySchedule.user_id == user_id)
        
        # 按班次类型筛选
        if shift_type:
            query = query.filter(DutySchedule.shift_type == shift_type)
        
        # 按状态筛选
        if status:
            query = query.filter(DutySchedule.status == status)
        
        # 按值班地点筛选
        if location:
            query = query.filter(DutySchedule.location.like(f'%{location}%'))
        
        # 按日期范围筛选
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
                query = query.filter(DutySchedule.duty_date >= start_dt)
            except ValueError:
                return api_error("开始日期格式错误，应为YYYY-MM-DD", 400)
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(DutySchedule.duty_date <= end_dt)
            except ValueError:
                return api_error("结束日期格式错误，应为YYYY-MM-DD", 400)
        
        # 按值班日期排序
        query = query.order_by(DutySchedule.duty_date.desc(), DutySchedule.shift_type.asc())
        
        # 分页查询
        total = query.count()
        schedules = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [schedule.to_dict() for schedule in schedules]
        
        return api_paginated_success(data, page, limit, total, "获取值班安排列表成功")
        
    except Exception as e:
        return api_error(f"获取值班安排列表失败: {str(e)}", 500)

@api_bp.route('/duty-schedules/<int:schedule_id>', methods=['GET'])
@jwt_required()
def get_duty_schedule_detail(schedule_id):
    """获取值班安排详情"""
    try:
        schedule = DutySchedule.query.get(schedule_id)
        
        if not schedule:
            return api_error("值班安排不存在", 404)
        
        return api_success(data=schedule.to_dict(), message="获取值班安排详情成功")
        
    except Exception as e:
        return api_error(f"获取值班安排详情失败: {str(e)}", 500)

@api_bp.route('/duty-schedules/<int:schedule_id>', methods=['PUT'])
@jwt_required()
def update_duty_schedule(schedule_id):
    """更新值班安排"""
    try:
        schedule = DutySchedule.query.get(schedule_id)
        
        if not schedule:
            return api_error("值班安排不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证用户是否存在（如果提供了用户ID）
        if 'user_id' in data:
            user = User.query.get(data['user_id'])
            if not user:
                return api_error("用户不存在", 400)
        
        # 验证班次类型
        if 'shift_type' in data and data['shift_type'] not in ['morning', 'afternoon', 'evening', 'night', 'full_day']:
            return api_error("班次类型必须是 morning, afternoon, evening, night, full_day 之一", 400)
        
        # 验证状态
        if 'status' in data and data['status'] not in ['scheduled', 'completed', 'absent', 'cancelled']:
            return api_error("状态必须是 scheduled, completed, absent, cancelled 之一", 400)
        
        # 解析值班日期
        if 'duty_date' in data:
            try:
                data['duty_date'] = datetime.strptime(data['duty_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("值班日期格式错误，应为YYYY-MM-DD", 400)
        
        # 检查是否已有相同用户在同一天同一班次的值班安排（排除当前记录）
        if 'user_id' in data or 'duty_date' in data or 'shift_type' in data:
            user_id = data.get('user_id', schedule.user_id)
            duty_date = data.get('duty_date', schedule.duty_date)
            shift_type = data.get('shift_type', schedule.shift_type)
            
            existing_schedule = DutySchedule.query.filter(
                DutySchedule.user_id == user_id,
                DutySchedule.duty_date == duty_date,
                DutySchedule.shift_type == shift_type,
                DutySchedule.id != schedule_id
            ).first()
            
            if existing_schedule:
                return api_error("该用户在此日期此班次已有值班安排", 400)
        
        # 解析签到时间
        if 'check_in_time' in data and data['check_in_time']:
            try:
                data['check_in_time'] = datetime.strptime(data['check_in_time'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return api_error("签到时间格式错误，应为YYYY-MM-DD HH:MM:SS", 400)
        
        # 解析签退时间
        if 'check_out_time' in data and data['check_out_time']:
            try:
                data['check_out_time'] = datetime.strptime(data['check_out_time'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return api_error("签退时间格式错误，应为YYYY-MM-DD HH:MM:SS", 400)
        
        # 更新字段
        for field in ['user_id', 'duty_date', 'shift_type', 'location', 'status', 
                     'check_in_time', 'check_out_time', 'notes']:
            if field in data:
                setattr(schedule, field, data[field])
        
        db.session.commit()
        
        return api_success(data=schedule.to_dict(), message="更新值班安排成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新值班安排失败: {str(e)}", 500)

@api_bp.route('/duty-schedules/<int:schedule_id>/check-in', methods=['PUT'])
@jwt_required()
def check_in_duty(schedule_id):
    """值班签到"""
    try:
        current_user_id = get_jwt_identity()
        schedule = DutySchedule.query.get(schedule_id)
        
        if not schedule:
            return api_error("值班安排不存在", 404)
        
        # 检查权限：只有值班人员可以签到
        if schedule.user_id != current_user_id:
            return api_error("只有值班人员可以签到", 403)
        
        # 检查是否已签到
        if schedule.check_in_time:
            return api_error("已经签到过了", 400)
        
        # 检查值班日期
        today = date.today()
        if schedule.duty_date != today:
            return api_error("只能在值班当天签到", 400)
        
        # 签到
        schedule.check_in_time = beijing_now()
        schedule.status = 'completed'  # 签到后状态变为已完成
        
        db.session.commit()
        
        return api_success(data=schedule.to_dict(), message="值班签到成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"值班签到失败: {str(e)}", 500)

@api_bp.route('/duty-schedules/<int:schedule_id>/check-out', methods=['PUT'])
@jwt_required()
def check_out_duty(schedule_id):
    """值班签退"""
    try:
        current_user_id = get_jwt_identity()
        schedule = DutySchedule.query.get(schedule_id)
        
        if not schedule:
            return api_error("值班安排不存在", 404)
        
        # 检查权限：只有值班人员可以签退
        if schedule.user_id != current_user_id:
            return api_error("只有值班人员可以签退", 403)
        
        # 检查是否已签到
        if not schedule.check_in_time:
            return api_error("请先签到", 400)
        
        # 检查是否已签退
        if schedule.check_out_time:
            return api_error("已经签退过了", 400)
        
        # 签退
        schedule.check_out_time = beijing_now()
        
        db.session.commit()
        
        return api_success(data=schedule.to_dict(), message="值班签退成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"值班签退失败: {str(e)}", 500)

@api_bp.route('/duty-schedules/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
def delete_duty_schedule(schedule_id):
    """删除值班安排"""
    try:
        schedule = DutySchedule.query.get(schedule_id)
        
        if not schedule:
            return api_error("值班安排不存在", 404)
        
        # 只有未开始的值班安排可以删除
        if schedule.status not in ['scheduled']:
            return api_error("只有计划中的值班安排可以删除", 400)
        
        db.session.delete(schedule)
        db.session.commit()
        
        return api_success(message="删除值班安排成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除值班安排失败: {str(e)}", 500)

@api_bp.route('/duty-schedules/calendar', methods=['GET'])
@jwt_required()
def get_duty_calendar():
    """获取值班日历"""
    try:
        # 获取查询参数
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        user_id = request.args.get('user_id', type=int)
        
        # 验证年月参数
        if not (1 <= month <= 12):
            return api_error("月份必须在1-12之间", 400)
        
        # 计算月份的开始和结束日期
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        # 构建查询
        query = DutySchedule.query.filter(
            DutySchedule.duty_date >= start_date,
            DutySchedule.duty_date <= end_date
        )
        
        # 按用户筛选
        if user_id:
            query = query.filter(DutySchedule.user_id == user_id)
        
        # 获取值班安排
        schedules = query.order_by(DutySchedule.duty_date.asc(), DutySchedule.shift_type.asc()).all()
        
        # 按日期组织数据
        calendar_data = {}
        for schedule in schedules:
            date_str = schedule.duty_date.strftime('%Y-%m-%d')
            if date_str not in calendar_data:
                calendar_data[date_str] = []
            calendar_data[date_str].append(schedule.to_dict())
        
        return api_success(data=calendar_data, message="获取值班日历成功")
        
    except Exception as e:
        return api_error(f"获取值班日历失败: {str(e)}", 500)

@api_bp.route('/duty-schedules/statistics', methods=['GET'])
@jwt_required()
def get_duty_statistics():
    """获取值班统计"""
    try:
        period = request.args.get('period', 'month')
        user_id = request.args.get('user_id', type=int)
        
        # 时间范围
        now = datetime.now()
        if period == 'day':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now.weekday())
        else:  # month
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        start_date = start_time.date()
        
        # 基础统计
        query = DutySchedule.query
        if user_id:
            query = query.filter(DutySchedule.user_id == user_id)
        
        total_schedules = query.count()
        completed_schedules = query.filter(DutySchedule.status == 'completed').count()
        absent_schedules = query.filter(DutySchedule.status == 'absent').count()
        cancelled_schedules = query.filter(DutySchedule.status == 'cancelled').count()
        
        # 时间范围内统计
        period_query = query.filter(DutySchedule.duty_date >= start_date)
        period_total = period_query.count()
        period_completed = period_query.filter(DutySchedule.status == 'completed').count()
        period_absent = period_query.filter(DutySchedule.status == 'absent').count()
        
        # 出勤率
        attendance_rate = (completed_schedules / total_schedules * 100) if total_schedules > 0 else 0
        period_attendance_rate = (period_completed / period_total * 100) if period_total > 0 else 0
        
        # 班次分布
        shift_stats = db.session.query(
            DutySchedule.shift_type,
            func.count(DutySchedule.id).label('count')
        ).group_by(DutySchedule.shift_type)
        
        if user_id:
            shift_stats = shift_stats.filter(DutySchedule.user_id == user_id)
        
        shift_distribution = {
            item.shift_type: item.count
            for item in shift_stats.all()
        }
        
        # 用户值班统计
        user_stats = db.session.query(
            User.id,
            User.full_name,
            func.count(DutySchedule.id).label('total_schedules'),
            func.sum(func.case([(DutySchedule.status == 'completed', 1)], else_=0)).label('completed_schedules'),
            func.sum(func.case([(DutySchedule.status == 'absent', 1)], else_=0)).label('absent_schedules')
        ).join(DutySchedule, User.id == DutySchedule.user_id).group_by(
            User.id, User.full_name
        ).all()
        
        user_performance = [
            {
                'user_id': item.id,
                'user_name': item.full_name,
                'total_schedules': item.total_schedules,
                'completed_schedules': item.completed_schedules or 0,
                'absent_schedules': item.absent_schedules or 0,
                'attendance_rate': (item.completed_schedules or 0) / item.total_schedules * 100 if item.total_schedules > 0 else 0
            }
            for item in user_stats
        ]
        
        # 今日值班
        today = date.today()
        today_schedules = DutySchedule.query.filter(
            DutySchedule.duty_date == today
        ).order_by(DutySchedule.shift_type.asc()).all()
        
        today_duty = [schedule.to_dict() for schedule in today_schedules]
        
        data = {
            'total_schedules': total_schedules,
            'completed_schedules': completed_schedules,
            'absent_schedules': absent_schedules,
            'cancelled_schedules': cancelled_schedules,
            f'{period}_total': period_total,
            f'{period}_completed': period_completed,
            f'{period}_absent': period_absent,
            'attendance_rate': round(attendance_rate, 2),
            f'{period}_attendance_rate': round(period_attendance_rate, 2),
            'shift_distribution': shift_distribution,
            'user_performance': user_performance,
            'today_duty': today_duty
        }
        
        return api_success(data=data, message="获取值班统计成功")
        
    except Exception as e:
        return api_error(f"获取值班统计失败: {str(e)}", 500)