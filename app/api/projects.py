#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 项目成果API
"""

from flask import request
from flask_jwt_extended import jwt_required
from app.api import api_bp
from app.models import Project, ProjectMember, User
from app import db
from app.helpers.responses import api_success, api_error, api_paginated_success
from datetime import datetime

@api_bp.route('/projects', methods=['GET'])
def get_projects():
    """获取项目成果列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        achievement_type = request.args.get('achievement_type')
        
        # 构建查询
        query = Project.query
        
        # 按成果类型筛选
        if achievement_type:
            query = query.filter(Project.achievement_type == achievement_type)
        
        # 按项目开始日期倒序排列（MySQL兼容）
        query = query.order_by(Project.start_date.desc())
        
        # 分页查询
        total = query.count()
        projects = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [project.to_dict() for project in projects]
        
        return api_paginated_success(data, page, limit, total, "获取项目成果列表成功")
        
    except Exception as e:
        return api_error(f"获取项目成果列表失败: {str(e)}", 500)

@api_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    """创建项目成果"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['project_name', 'achievement_type']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"{field}不能为空", 400)
        
        # 验证成果类型是否有效
        valid_types = ['获奖', '专利', '软著']
        if data['achievement_type'] not in valid_types:
            return api_error(f"无效的成果类型，有效类型: {', '.join(valid_types)}", 400)
        
        # 解析日期
        start_date = None
        end_date = None
        
        if data.get('start_date'):
            try:
                start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("开始日期格式错误，应为YYYY-MM-DD", 400)
        
        if data.get('end_date'):
            try:
                end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("结束日期格式错误，应为YYYY-MM-DD", 400)
        
        # 创建新项目
        project = Project(
            project_name=data['project_name'],
            description=data.get('description'),
            achievement_type=data['achievement_type'],
            achievement_details=data.get('achievement_details'),
            start_date=start_date,
            end_date=end_date,
            image_url=data.get('image_url')
        )
        
        db.session.add(project)
        db.session.flush()  # 获取项目ID
        
        # 处理项目成员
        members_data = data.get('members', [])
        for member_data in members_data:
            user_id = member_data.get('user_id')
            if not user_id:
                continue
            
            # 验证用户是否存在
            user = User.query.get(user_id)
            if not user:
                return api_error(f"用户ID {user_id} 不存在", 400)
            
            # 创建项目成员关联
            project_member = ProjectMember(
                project_id=project.id,
                user_id=user_id,
                role_in_project=member_data.get('role_in_project')
            )
            db.session.add(project_member)
        
        db.session.commit()
        
        return api_success(data=project.to_dict(), message="创建项目成果成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建项目成果失败: {str(e)}", 500)

@api_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """获取单个项目成果详情"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return api_error("项目成果不存在", 404)
        
        return api_success(data=project.to_dict(), message="获取项目成果详情成功")
        
    except Exception as e:
        return api_error(f"获取项目成果详情失败: {str(e)}", 500)

@api_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """更新项目成果"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return api_error("项目成果不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证成果类型是否有效（如果提供了类型）
        if 'achievement_type' in data:
            valid_types = ['获奖', '专利', '软著']
            if data['achievement_type'] not in valid_types:
                return api_error(f"无效的成果类型，有效类型: {', '.join(valid_types)}", 400)
        
        # 解析日期
        if 'start_date' in data and data['start_date']:
            try:
                data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("开始日期格式错误，应为YYYY-MM-DD", 400)
        
        if 'end_date' in data and data['end_date']:
            try:
                data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("结束日期格式错误，应为YYYY-MM-DD", 400)
        
        # 更新项目基本信息
        updatable_fields = ['project_name', 'description', 'achievement_type', 
                           'achievement_details', 'start_date', 'end_date', 'image_url']
        for field in updatable_fields:
            if field in data:
                setattr(project, field, data[field])
        
        # 处理项目成员更新
        if 'members' in data:
            # 删除现有成员
            ProjectMember.query.filter_by(project_id=project.id).delete()
            
            # 添加新成员
            members_data = data['members']
            for member_data in members_data:
                user_id = member_data.get('user_id')
                if not user_id:
                    continue
                
                # 验证用户是否存在
                user = User.query.get(user_id)
                if not user:
                    return api_error(f"用户ID {user_id} 不存在", 400)
                
                # 创建项目成员关联
                project_member = ProjectMember(
                    project_id=project.id,
                    user_id=user_id,
                    role_in_project=member_data.get('role_in_project')
                )
                db.session.add(project_member)
        
        db.session.commit()
        
        return api_success(data=project.to_dict(), message="更新项目成果成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新项目成果失败: {str(e)}", 500)

@api_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """删除项目成果"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return api_error("项目成果不存在", 404)
        
        # 删除项目（级联删除成员关联）
        db.session.delete(project)
        db.session.commit()
        
        return api_success(message="删除项目成果成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除项目成果失败: {str(e)}", 500)