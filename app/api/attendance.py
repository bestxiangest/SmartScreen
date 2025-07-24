#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 考勤管理API
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models import AttendanceLog, User, beijing_now
from app.extensions import db
from app.helpers.responses import api_success, api_error, api_paginated_success
from datetime import datetime, date
import hashlib
import json
import qrcode
import io
import base64

@api_bp.route('/attendance', methods=['GET'])
@jwt_required()
def get_attendance_logs():
    """获取考勤记录列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        user_id = request.args.get('user_id', type=int)
        date_str = request.args.get('date')
        method = request.args.get('method')
        
        # 构建查询
        query = AttendanceLog.query
        
        # 按用户筛选
        if user_id:
            query = query.filter(AttendanceLog.user_id == user_id)
        
        # 按日期筛选
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                query = query.filter(
                    db.func.date(AttendanceLog.check_in_time) == target_date
                )
            except ValueError:
                return api_error("日期格式错误，应为YYYY-MM-DD", 400)
        
        # 按考勤方式筛选
        if method:
            valid_methods = ['人脸识别', '扫码', '手动']
            if method not in valid_methods:
                return api_error(f"无效的考勤方式，有效方式: {', '.join(valid_methods)}", 400)
            query = query.filter(AttendanceLog.method == method)
        
        # 按签到时间倒序排列
        query = query.order_by(AttendanceLog.check_in_time.desc())
        
        # 分页查询
        total = query.count()
        logs = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [log.to_dict() for log in logs]
        
        return api_paginated_success(data, page, limit, total, "获取考勤记录列表成功")
        
    except Exception as e:
        return api_error(f"获取考勤记录列表失败: {str(e)}", 500)

@api_bp.route('/attendance/check-in', methods=['POST'])
@jwt_required()
def check_in():
    """签到"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        
        # 验证考勤方式
        method = data.get('method', '手动')
        valid_methods = ['人脸识别', '扫码', '手动']
        if method not in valid_methods:
            return api_error(f"无效的考勤方式，有效方式: {', '.join(valid_methods)}", 400)
        
        # 检查今日是否已签到
        today = beijing_now().date()
        existing_log = AttendanceLog.query.filter(
            AttendanceLog.user_id == current_user_id,
            db.func.date(AttendanceLog.check_in_time) == today
        ).first()
        
        if existing_log:
            return api_error("今日已签到", 400)
        
        # 创建签到记录
        attendance_log = AttendanceLog(
            user_id=current_user_id,
            method=method,
            emotion_status=data.get('emotion_status')
        )
        
        db.session.add(attendance_log)
        db.session.commit()
        
        return api_success(data=attendance_log.to_dict(), message="签到成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"签到失败: {str(e)}", 500)

@api_bp.route('/attendance/admin/check-in', methods=['POST'])
@jwt_required()
def admin_check_in():
    """管理员控制的签到"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        user_id = data.get('user_id')
        if not user_id:
            return api_error("用户ID不能为空", 400)
        
        # 验证用户是否存在
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 验证考勤方式
        method = data.get('method', '手动')
        valid_methods = ['人脸识别', '扫码', '手动']
        if method not in valid_methods:
            return api_error(f"无效的考勤方式，有效方式: {', '.join(valid_methods)}", 400)
        
        # 检查今日是否已签到
        today = beijing_now().date()
        existing_log = AttendanceLog.query.filter(
            AttendanceLog.user_id == user_id,
            db.func.date(AttendanceLog.check_in_time) == today
        ).first()
        
        if existing_log:
            return api_error(f"用户 {user.full_name} 今日已签到", 400)
        
        # 创建签到记录
        attendance_log = AttendanceLog(
            user_id=user_id,
            method=method,
            emotion_status=data.get('emotion_status')
        )
        
        db.session.add(attendance_log)
        db.session.commit()
        
        return api_success(data=attendance_log.to_dict(), message=f"管理员为 {user.full_name} 签到成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"管理员签到失败: {str(e)}", 500)

@api_bp.route('/attendance/admin/check-out', methods=['POST'])
@jwt_required()
def admin_check_out():
    """管理员控制的签退"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        user_id = data.get('user_id')
        if not user_id:
            return api_error("用户ID不能为空", 400)
        
        # 验证用户是否存在
        user = User.query.get(user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 查找今日签到记录
        today = beijing_now().date()
        attendance_log = AttendanceLog.query.filter(
            AttendanceLog.user_id == user_id,
            db.func.date(AttendanceLog.check_in_time) == today
        ).first()
        
        if not attendance_log:
            return api_error(f"用户 {user.full_name} 今日未签到，无法签退", 400)
        
        # 检查是否已签退
        if attendance_log.check_out_time:
            return api_error(f"用户 {user.full_name} 已签退", 400)
        
        # 更新签退时间
        attendance_log.check_out_time = beijing_now()
        
        db.session.commit()
        
        return api_success(data=attendance_log.to_dict(), message=f"管理员为 {user.full_name} 签退成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"管理员签退失败: {str(e)}", 500)

@api_bp.route('/attendance/<int:log_id>/check-out', methods=['PUT'])
@jwt_required()
def check_out(log_id):
    """签出"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # 查找签到记录
        attendance_log = AttendanceLog.query.get(log_id)
        
        if not attendance_log:
            return api_error("考勤记录不存在", 404)
        
        # 验证是否为当前用户的记录
        if attendance_log.user_id != current_user_id:
            return api_error("只能操作自己的考勤记录", 403)
        
        # 检查是否已签出
        if attendance_log.check_out_time:
            return api_error("已签出", 400)
        
        # 更新签退时间
        attendance_log.check_out_time = beijing_now()
        
        db.session.commit()
        
        return api_success(data=attendance_log.to_dict(), message="签出成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"签出失败: {str(e)}", 500)

@api_bp.route('/attendance/today', methods=['GET'])
@jwt_required()
def get_today_attendance():
    """获取今日考勤状态"""
    try:
        current_user_id = int(get_jwt_identity())
        today = beijing_now().date()
        
        # 查找今日考勤记录
        attendance_log = AttendanceLog.query.filter(
            AttendanceLog.user_id == current_user_id,
            db.func.date(AttendanceLog.check_in_time) == today
        ).first()
        
        if not attendance_log:
            return api_success(data=None, message="今日未签到")
        
        return api_success(data=attendance_log.to_dict(), message="获取今日考勤状态成功")
        
    except Exception as e:
        return api_error(f"获取今日考勤状态失败: {str(e)}", 500)

@api_bp.route('/attendance/statistics', methods=['GET'])
@jwt_required()
def get_attendance_statistics():
    """获取考勤统计"""
    try:
        # 获取查询参数
        user_id = request.args.get('user_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 如果没有指定用户，则统计当前用户
        if not user_id:
            user_id = int(get_jwt_identity())
        
        # 构建查询
        query = AttendanceLog.query.filter(AttendanceLog.user_id == user_id)
        
        # 按日期范围筛选
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                query = query.filter(
                    db.func.date(AttendanceLog.check_in_time) >= start_date_obj
                )
            except ValueError:
                return api_error("开始日期格式错误，应为YYYY-MM-DD", 400)
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(
                    db.func.date(AttendanceLog.check_in_time) <= end_date_obj
                )
            except ValueError:
                return api_error("结束日期格式错误，应为YYYY-MM-DD", 400)
        
        # 统计数据
        total_days = query.count()
        checked_out_days = query.filter(AttendanceLog.check_out_time.isnot(None)).count()
        
        # 按考勤方式统计
        method_stats = db.session.query(
            AttendanceLog.method,
            db.func.count(AttendanceLog.id).label('count')
        ).filter(
            AttendanceLog.user_id == user_id
        )
        
        if start_date:
            method_stats = method_stats.filter(
                db.func.date(AttendanceLog.check_in_time) >= start_date_obj
            )
        
        if end_date:
            method_stats = method_stats.filter(
                db.func.date(AttendanceLog.check_in_time) <= end_date_obj
            )
        
        method_stats = method_stats.group_by(AttendanceLog.method).all()
        
        statistics = {
            'total_attendance_days': total_days,
            'completed_days': checked_out_days,
            'incomplete_days': total_days - checked_out_days,
            'method_statistics': {
                method: count for method, count in method_stats
            }
        }
        
        return api_success(data=statistics, message="获取考勤统计成功")
        
    except Exception as e:
        return api_error(f"获取考勤统计失败: {str(e)}", 500)

@api_bp.route('/attendance/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_attendance_log(log_id):
    """删除考勤记录（管理员功能）"""
    try:
        attendance_log = AttendanceLog.query.get(log_id)
        
        if not attendance_log:
            return api_error("考勤记录不存在", 404)
        
        db.session.delete(attendance_log)
        db.session.commit()
        
        return api_success(message="删除考勤记录成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除考勤记录失败: {str(e)}", 500)

@api_bp.route('/attendance/qr-code', methods=['GET'])
def generate_qr_code():
    """生成每日二维码"""
    try:
        # 获取当前日期
        today = beijing_now().date().isoformat()
        
        # 生成每日唯一的token
        secret_key = "smartscreen_attendance_2024"  # 应该从配置文件读取
        token_data = f"{today}_{secret_key}"
        daily_token = hashlib.sha256(token_data.encode()).hexdigest()[:16]
        
        # 构建二维码数据
        qr_data = {
            "type": "attendance_checkin",
            "date": today,
            "token": daily_token
        }
        
        # 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        # 创建二维码图片
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 转换为base64
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return api_success(data={
            "qr_code_image": f"data:image/png;base64,{img_str}",
            "token": daily_token,
            "date": today,
            "expires_at": f"{today} 23:59:59"
        }, message="生成二维码成功")
        
    except Exception as e:
        return api_error(f"生成二维码失败: {str(e)}", 500)

@api_bp.route('/attendance/qr-code-url', methods=['POST'])
def generate_qr_code_with_url():
    """生成包含URL的二维码"""
    try:
        data = request.get_json() or {}
        url = data.get('url')
        token = data.get('token')
        date_str = data.get('date')
        
        if not url or not token or not date_str:
            return api_error("缺少必要参数", 400)
        
        # 验证token是否有效
        today = beijing_now().date().isoformat()
        if date_str != today:
            return api_error("日期无效", 400)
            
        secret_key = "smartscreen_attendance_2024"
        token_data = f"{today}_{secret_key}"
        valid_token = hashlib.sha256(token_data.encode()).hexdigest()[:16]
        
        if token != valid_token:
            return api_error("token无效", 400)
        
        # 生成包含URL的二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # 创建二维码图片
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 转换为base64
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return api_success(data={
            "qr_code_image": f"data:image/png;base64,{img_str}",
            "url": url,
            "token": token,
            "date": date_str
        }, message="生成URL二维码成功")
        
    except Exception as e:
        return api_error(f"生成二维码失败: {str(e)}", 500)


@api_bp.route('/attendance/qr-checkin', methods=['POST'])
def qr_code_checkin():
    """二维码签到（无需JWT认证）"""
    try:
        data = request.get_json() or {}
        
        # 记录接收到的数据用于调试
        print(f"[DEBUG] 接收到的签到数据: {data}")
        
        # 获取参数
        token = data.get('token')
        user_name = data.get('user_name', '').strip()
        emotion_status = data.get('emotion_status')
        
        print(f"[DEBUG] 解析后的参数 - token: {token}, user_name: '{user_name}', emotion_status: {emotion_status}")
        
        if not token:
            return api_error("缺少二维码token", 400)
        
        if not user_name:
            return api_error("请填写姓名", 400)
        
        # 验证token是否为今日有效token
        today = date.today().isoformat()
        secret_key = "smartscreen_attendance_2024"
        token_data = f"{today}_{secret_key}"
        valid_token = hashlib.sha256(token_data.encode()).hexdigest()[:16]
        
        if token != valid_token:
            return api_error("二维码已过期或无效", 400)
        
        # 根据姓名查找用户
        print(f"[DEBUG] 正在查找用户，姓名: '{user_name}', 长度: {len(user_name)}")
        user = User.query.filter_by(full_name=user_name).first()
        
        if not user:
            # 查找所有相似的用户名用于调试
            similar_users = User.query.filter(User.full_name.like(f'%{user_name}%')).all()
            print(f"[DEBUG] 未找到精确匹配的用户，相似用户: {[(u.id, u.full_name, len(u.full_name)) for u in similar_users]}")
            
            # 查找所有用户用于调试
            all_users = User.query.all()
            print(f"[DEBUG] 数据库中所有用户: {[(u.id, u.full_name) for u in all_users]}")
            
            return api_error("用户不存在，请检查姓名是否正确", 404)
        
        print(f"[DEBUG] 找到用户: ID={user.id}, 姓名='{user.full_name}'")
        
        # 检查今日是否已签到
        today_date = date.today()
        existing_log = AttendanceLog.query.filter(
            AttendanceLog.user_id == user.id,
            db.func.date(AttendanceLog.check_in_time) == today_date
        ).first()
        
        if existing_log:
            return api_error("今日已签到", 400)
        
        # 创建签到记录
        attendance_log = AttendanceLog(
            user_id=user.id,
            method='扫码',
            emotion_status=emotion_status
        )
        
        db.session.add(attendance_log)
        db.session.commit()
        
        return api_success(data={
            "user_name": user.full_name,
            "check_in_time": attendance_log.check_in_time.isoformat(),
            "method": "扫码"
        }, message=f"{user.full_name} 签到成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"签到失败: {str(e)}", 500)