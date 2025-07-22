#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - AI个性化培养方案API
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models import AITrainingPlan, User
from app.extensions import db
from app.helpers.responses import api_success, api_error, api_paginated_success
import json

@api_bp.route('/v1/ai-training-plans', methods=['GET'])
@jwt_required()
def get_ai_training_plans():
    """获取AI培养方案列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        user_id = request.args.get('user_id', type=int)
        status = request.args.get('status')
        
        # 构建查询
        query = AITrainingPlan.query
        
        # 按用户筛选
        if user_id:
            query = query.filter(AITrainingPlan.user_id == user_id)
        
        # 按状态筛选
        if status:
            valid_statuses = ['进行中', '已完成']
            if status not in valid_statuses:
                return api_error(f"无效的状态，有效状态: {', '.join(valid_statuses)}", 400)
            query = query.filter(AITrainingPlan.status == status)
        
        # 按生成时间倒序排列
        query = query.order_by(AITrainingPlan.generated_at.desc())
        
        # 分页查询
        total = query.count()
        plans = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [plan.to_dict() for plan in plans]
        
        return api_paginated_success(data, page, limit, total, "获取AI培养方案列表成功")
        
    except Exception as e:
        return api_error(f"获取AI培养方案列表失败: {str(e)}", 500)

@api_bp.route('/v1/ai-training-plans', methods=['POST'])
@jwt_required()
def create_ai_training_plan():
    """创建AI培养方案"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        if not data.get('plan_content'):
            return api_error("培养方案内容不能为空", 400)
        
        # 获取目标用户ID，如果没有指定则为当前用户
        target_user_id = data.get('user_id', int(get_jwt_identity()))
        
        # 验证用户是否存在
        user = User.query.get(target_user_id)
        if not user:
            return api_error("目标用户不存在", 400)
        
        # 处理培养方案内容JSON数据
        plan_content = data['plan_content']
        if isinstance(plan_content, str):
            try:
                plan_content = json.loads(plan_content)
            except json.JSONDecodeError:
                return api_error("培养方案内容格式错误", 400)
        
        # 验证状态是否有效
        status = data.get('status', '进行中')
        valid_statuses = ['进行中', '已完成']
        if status not in valid_statuses:
            return api_error(f"无效的状态，有效状态: {', '.join(valid_statuses)}", 400)
        
        # 创建新培养方案
        training_plan = AITrainingPlan(
            user_id=target_user_id,
            plan_content=plan_content,
            status=status
        )
        
        db.session.add(training_plan)
        db.session.commit()
        
        return api_success(data=training_plan.to_dict(), message="创建AI培养方案成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建AI培养方案失败: {str(e)}", 500)

@api_bp.route('/v1/ai-training-plans/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_ai_training_plan(plan_id):
    """获取单个AI培养方案详情"""
    try:
        plan = AITrainingPlan.query.get(plan_id)
        
        if not plan:
            return api_error("AI培养方案不存在", 404)
        
        return api_success(data=plan.to_dict(), message="获取AI培养方案详情成功")
        
    except Exception as e:
        return api_error(f"获取AI培养方案详情失败: {str(e)}", 500)

@api_bp.route('/v1/ai-training-plans/<int:plan_id>', methods=['PUT'])
@jwt_required()
def update_ai_training_plan(plan_id):
    """更新AI培养方案"""
    try:
        plan = AITrainingPlan.query.get(plan_id)
        
        if not plan:
            return api_error("AI培养方案不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 处理培养方案内容JSON数据
        if 'plan_content' in data:
            plan_content = data['plan_content']
            if isinstance(plan_content, str):
                try:
                    plan_content = json.loads(plan_content)
                    data['plan_content'] = plan_content
                except json.JSONDecodeError:
                    return api_error("培养方案内容格式错误", 400)
        
        # 验证状态是否有效
        if 'status' in data:
            valid_statuses = ['进行中', '已完成']
            if data['status'] not in valid_statuses:
                return api_error(f"无效的状态，有效状态: {', '.join(valid_statuses)}", 400)
        
        # 更新字段
        updatable_fields = ['plan_content', 'status']
        for field in updatable_fields:
            if field in data:
                setattr(plan, field, data[field])
        
        db.session.commit()
        
        return api_success(data=plan.to_dict(), message="更新AI培养方案成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新AI培养方案失败: {str(e)}", 500)

@api_bp.route('/v1/ai-training-plans/<int:plan_id>', methods=['DELETE'])
@jwt_required()
def delete_ai_training_plan(plan_id):
    """删除AI培养方案"""
    try:
        plan = AITrainingPlan.query.get(plan_id)
        
        if not plan:
            return api_error("AI培养方案不存在", 404)
        
        db.session.delete(plan)
        db.session.commit()
        
        return api_success(message="删除AI培养方案成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除AI培养方案失败: {str(e)}", 500)

@api_bp.route('/v1/ai-training-plans/my-plans', methods=['GET'])
@jwt_required()
def get_my_training_plans():
    """获取当前用户的培养方案"""
    try:
        current_user_id = int(get_jwt_identity())
        
        plans = AITrainingPlan.query.filter(
            AITrainingPlan.user_id == current_user_id
        ).order_by(AITrainingPlan.generated_at.desc()).all()
        
        data = [plan.to_dict() for plan in plans]
        
        return api_success(data=data, message="获取我的培养方案成功")
        
    except Exception as e:
        return api_error(f"获取我的培养方案失败: {str(e)}", 500)

@api_bp.route('/v1/ai-training-plans/generate', methods=['POST'])
@jwt_required()
def generate_ai_training_plan():
    """AI生成个性化培养方案"""
    try:
        data = request.get_json() or {}
        current_user_id = int(get_jwt_identity())
        
        # 获取用户信息
        user = User.query.get(current_user_id)
        if not user:
            return api_error("用户不存在", 404)
        
        # 这里应该调用AI服务生成个性化方案
        # 目前使用模拟数据
        ai_generated_plan = {
            "learning_objectives": [
                "掌握Python编程基础",
                "学习机器学习算法",
                "实践深度学习项目"
            ],
            "study_schedule": {
                "duration": "3个月",
                "weekly_hours": 10,
                "milestones": [
                    {
                        "week": 4,
                        "goal": "完成Python基础学习"
                    },
                    {
                        "week": 8,
                        "goal": "掌握机器学习基础算法"
                    },
                    {
                        "week": 12,
                        "goal": "完成深度学习项目"
                    }
                ]
            },
            "recommended_resources": [
                "Python官方文档",
                "机器学习实战",
                "深度学习课程"
            ],
            "assessment_criteria": [
                "编程能力测试",
                "项目完成质量",
                "理论知识掌握"
            ]
        }
        
        # 创建培养方案
        training_plan = AITrainingPlan(
            user_id=current_user_id,
            plan_content=ai_generated_plan,
            status='进行中'
        )
        
        db.session.add(training_plan)
        db.session.commit()
        
        return api_success(data=training_plan.to_dict(), message="AI培养方案生成成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"AI培养方案生成失败: {str(e)}", 500)