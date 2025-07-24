#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 环境监测API
"""

from flask import request
from flask_jwt_extended import jwt_required
from app.api import api_bp
from app.models import EnvironmentalLog, Lab, beijing_now
from app.extensions import db
from app.helpers.responses import api_success, api_error, api_paginated_success
from datetime import datetime, timedelta
from sqlalchemy import func

@api_bp.route('/environmental/data', methods=['GET'])
@jwt_required()
def get_environmental_logs():
    """获取环境监测日志列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        sensor_type = request.args.get('sensor_type')
        lab_id = request.args.get('lab_id', type=int)
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        # 构建查询
        query = EnvironmentalLog.query
        
        # 按传感器类型筛选
        if sensor_type:
            valid_types = ['温度', '湿度', '光照', 'CO2']
            if sensor_type not in valid_types:
                return api_error(f"无效的传感器类型，有效类型: {', '.join(valid_types)}", 400)
            query = query.filter(EnvironmentalLog.sensor_type == sensor_type)
        
        # 按实验室筛选
        if lab_id:
            query = query.filter(EnvironmentalLog.lab_id == lab_id)
        
        # 按时间范围筛选
        if start_time:
            try:
                start_datetime = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                query = query.filter(EnvironmentalLog.timestamp >= start_datetime)
            except ValueError:
                return api_error("开始时间格式错误，应为ISO格式", 400)
        
        if end_time:
            try:
                end_datetime = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                query = query.filter(EnvironmentalLog.timestamp <= end_datetime)
            except ValueError:
                return api_error("结束时间格式错误，应为ISO格式", 400)
        
        # 按时间倒序排列
        query = query.order_by(EnvironmentalLog.timestamp.desc())
        
        # 分页查询
        total = query.count()
        logs = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [log.to_dict() for log in logs]
        
        return api_paginated_success(data, page, limit, total, "获取环境监测日志列表成功")
        
    except Exception as e:
        return api_error(f"获取环境监测日志列表失败: {str(e)}", 500)

@api_bp.route('/environmental/data', methods=['POST'])
@jwt_required()
def create_environmental_log():
    """创建环境监测日志"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['sensor_type', 'value', 'unit', 'lab_id']
        for field in required_fields:
            if field not in data or data[field] is None:
                return api_error(f"{field}不能为空", 400)
        
        # 验证传感器类型
        valid_types = ['温度', '湿度', '光照', 'CO2']
        if data['sensor_type'] not in valid_types:
            return api_error(f"无效的传感器类型，有效类型: {', '.join(valid_types)}", 400)
        
        # 验证实验室是否存在
        lab = Lab.query.get(data['lab_id'])
        if not lab:
            return api_error("实验室不存在", 400)
        
        # 验证数值
        try:
            value = float(data['value'])
        except (ValueError, TypeError):
            return api_error("监测数值必须为数字", 400)
        
        # 解析时间戳（如果提供）
        timestamp = beijing_now()
        if data.get('timestamp'):
            try:
                timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            except ValueError:
                return api_error("时间戳格式错误，应为ISO格式", 400)
        
        # 创建新环境监测日志
        log = EnvironmentalLog(
            sensor_type=data['sensor_type'],
            value=value,
            unit=data['unit'],
            lab_id=data['lab_id'],
            timestamp=timestamp
        )
        
        db.session.add(log)
        db.session.commit()
        
        return api_success(data=log.to_dict(), message="创建环境监测日志成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建环境监测日志失败: {str(e)}", 500)

@api_bp.route('/environmental/data/<int:log_id>', methods=['GET'])
@jwt_required()
def get_environmental_log(log_id):
    """获取单个环境监测日志详情"""
    try:
        log = EnvironmentalLog.query.get(log_id)
        
        if not log:
            return api_error("环境监测日志不存在", 404)
        
        return api_success(data=log.to_dict(), message="获取环境监测日志详情成功")
        
    except Exception as e:
        return api_error(f"获取环境监测日志详情失败: {str(e)}", 500)

@api_bp.route('/environmental/data/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_environmental_log(log_id):
    """删除环境监测日志"""
    try:
        log = EnvironmentalLog.query.get(log_id)
        
        if not log:
            return api_error("环境监测日志不存在", 404)
        
        db.session.delete(log)
        db.session.commit()
        
        return api_success(message="删除环境监测日志成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除环境监测日志失败: {str(e)}", 500)

@api_bp.route('/environmental/data/latest', methods=['GET'])
@jwt_required()
def get_latest_environmental_data():
    """获取最新环境监测数据"""
    try:
        lab_id = request.args.get('lab_id', type=int)
        
        # 构建查询
        query = EnvironmentalLog.query
        
        if lab_id:
            query = query.filter(EnvironmentalLog.lab_id == lab_id)
        
        # 获取每种传感器类型的最新数据
        sensor_types = ['温度', '湿度', '光照', 'CO2']
        latest_data = {}
        
        for sensor_type in sensor_types:
            latest_log = query.filter(
                EnvironmentalLog.sensor_type == sensor_type
            ).order_by(EnvironmentalLog.timestamp.desc()).first()
            
            if latest_log:
                latest_data[sensor_type] = latest_log.to_dict()
        
        return api_success(data=latest_data, message="获取最新环境监测数据成功")
        
    except Exception as e:
        return api_error(f"获取最新环境监测数据失败: {str(e)}", 500)

@api_bp.route('/environmental/data/statistics', methods=['GET'])
@jwt_required()
def get_environmental_statistics():
    """获取环境监测统计数据"""
    try:
        # 获取查询参数
        sensor_type = request.args.get('sensor_type')
        lab_id = request.args.get('lab_id', type=int)
        hours = request.args.get('hours', 24, type=int)  # 默认统计最近24小时
        
        if not sensor_type:
            return api_error("传感器类型不能为空", 400)
        
        # 验证传感器类型
        valid_types = ['温度', '湿度', '光照', 'CO2']
        if sensor_type not in valid_types:
            return api_error(f"无效的传感器类型，有效类型: {', '.join(valid_types)}", 400)
        
        # 计算时间范围
        end_time = beijing_now()
        start_time = end_time - timedelta(hours=hours)
        
        # 构建查询
        query = EnvironmentalLog.query.filter(
            EnvironmentalLog.sensor_type == sensor_type,
            EnvironmentalLog.timestamp >= start_time,
            EnvironmentalLog.timestamp <= end_time
        )
        
        if lab_id:
            query = query.filter(EnvironmentalLog.lab_id == lab_id)
        
        # 计算统计数据
        stats = db.session.query(
            func.avg(EnvironmentalLog.value).label('avg_value'),
            func.min(EnvironmentalLog.value).label('min_value'),
            func.max(EnvironmentalLog.value).label('max_value'),
            func.count(EnvironmentalLog.id).label('count')
        ).filter(
            EnvironmentalLog.sensor_type == sensor_type,
            EnvironmentalLog.timestamp >= start_time,
            EnvironmentalLog.timestamp <= end_time
        )
        
        if lab_id:
            stats = stats.filter(EnvironmentalLog.lab_id == lab_id)
        
        result = stats.first()
        
        statistics = {
            'sensor_type': sensor_type,
            'time_range': {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'hours': hours
            },
            'average_value': float(result.avg_value) if result.avg_value else 0,
            'min_value': float(result.min_value) if result.min_value else 0,
            'max_value': float(result.max_value) if result.max_value else 0,
            'data_points': result.count or 0
        }
        
        return api_success(data=statistics, message="获取环境监测统计数据成功")
        
    except Exception as e:
        return api_error(f"获取环境监测统计数据失败: {str(e)}", 500)

@api_bp.route('/environmental/data/batch', methods=['POST'])
@jwt_required()
def create_batch_environmental_logs():
    """批量创建环境监测日志"""
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return api_error("请求数据必须为数组格式", 400)
        
        created_logs = []
        
        for log_data in data:
            # 验证必填字段
            required_fields = ['sensor_type', 'value', 'unit', 'lab_id']
            for field in required_fields:
                if field not in log_data or log_data[field] is None:
                    return api_error(f"记录中{field}不能为空", 400)
            
            # 验证传感器类型
            valid_types = ['温度', '湿度', '光照', 'CO2']
            if log_data['sensor_type'] not in valid_types:
                return api_error(f"无效的传感器类型，有效类型: {', '.join(valid_types)}", 400)
            
            # 验证实验室是否存在
            lab = Lab.query.get(log_data['lab_id'])
            if not lab:
                return api_error(f"实验室ID {log_data['lab_id']} 不存在", 400)
            
            # 验证数值
            try:
                value = float(log_data['value'])
            except (ValueError, TypeError):
                return api_error("监测数值必须为数字", 400)
            
            # 解析时间戳（如果提供）
            timestamp = beijing_now()
            if log_data.get('timestamp'):
                try:
                    timestamp = datetime.fromisoformat(log_data['timestamp'].replace('Z', '+00:00'))
                except ValueError:
                    return api_error("时间戳格式错误，应为ISO格式", 400)
            
            # 创建环境监测日志
            log = EnvironmentalLog(
                sensor_type=log_data['sensor_type'],
                value=value,
                unit=log_data['unit'],
                lab_id=log_data['lab_id'],
                timestamp=timestamp
            )
            
            db.session.add(log)
            created_logs.append(log)
        
        db.session.commit()
        
        # 转换为字典格式
        result_data = [log.to_dict() for log in created_logs]
        
        return api_success(data=result_data, message=f"批量创建{len(created_logs)}条环境监测日志成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"批量创建环境监测日志失败: {str(e)}", 500)