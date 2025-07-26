#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 仓库物料管理API
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import api_bp
from app.models import (
    MaterialCategory, Material, MaterialRequest, MaterialTransaction, 
    User, beijing_now
)
from app.extensions import db
from app.helpers.responses import api_success, api_error, api_paginated_success
from datetime import datetime, date, timedelta
from sqlalchemy import or_, and_, func
import json

# 物料分类相关接口
@api_bp.route('/material-categories', methods=['GET'])
@jwt_required()
def get_material_categories():
    """获取物料分类列表"""
    try:
        categories = MaterialCategory.query.order_by(MaterialCategory.sort_order.asc()).all()
        data = [category.to_dict() for category in categories]
        
        return api_success(data=data, message="获取物料分类列表成功")
        
    except Exception as e:
        return api_error(f"获取物料分类列表失败: {str(e)}", 500)

@api_bp.route('/material-categories', methods=['POST'])
@jwt_required()
def create_material_category():
    """创建物料分类"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return api_error("分类名称不能为空", 400)
        
        # 检查分类名称是否已存在
        existing_category = MaterialCategory.query.filter_by(
            name=data['name']
        ).first()
        
        if existing_category:
            return api_error("分类名称已存在", 400)
        
        category = MaterialCategory(
            name=data['name'],
            description=data.get('description'),
            parent_id=data.get('parent_id'),
            sort_order=data.get('sort_order', 0)
        )
        
        db.session.add(category)
        db.session.commit()
        
        return api_success(data=category.to_dict(), message="创建物料分类成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建物料分类失败: {str(e)}", 500)

@api_bp.route('/material-categories/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_material_category(category_id):
    """更新物料分类"""
    try:
        category = MaterialCategory.query.get(category_id)
        
        if not category:
            return api_error("物料分类不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 如果要更新名称，检查是否与其他分类重名
        if 'name' in data and data['name'] != category.name:
            existing_category = MaterialCategory.query.filter_by(
                name=data['name']
            ).first()
            
            if existing_category:
                return api_error("分类名称已存在", 400)
        
        # 更新字段
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        if 'parent_id' in data:
            category.parent_id = data['parent_id']
        if 'sort_order' in data:
            category.sort_order = data['sort_order']
        
        category.updated_at = beijing_now()
        
        db.session.commit()
        
        return api_success(data=category.to_dict(), message="更新物料分类成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新物料分类失败: {str(e)}", 500)

@api_bp.route('/material-categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_material_category(category_id):
    """删除物料分类"""
    try:
        category = MaterialCategory.query.get(category_id)
        
        if not category:
            return api_error("物料分类不存在", 404)
        
        # 检查是否有子分类
        child_categories = MaterialCategory.query.filter_by(parent_id=category_id).first()
        if child_categories:
            return api_error("该分类下存在子分类，无法删除", 400)
        
        # 检查是否有物料使用该分类
        materials = Material.query.filter_by(category_id=category_id).first()
        if materials:
            return api_error("该分类下存在物料，无法删除", 400)
        
        db.session.delete(category)
        db.session.commit()
        
        return api_success(message="删除物料分类成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除物料分类失败: {str(e)}", 500)

# 物料相关接口
@api_bp.route('/materials', methods=['GET'])
@jwt_required()
def get_materials():
    """获取物料列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        category_id = request.args.get('category_id', type=int)
        keyword = request.args.get('keyword')
        status = request.args.get('status')
        location = request.args.get('location')
        
        # 构建查询
        query = Material.query
        
        # 按分类筛选
        if category_id:
            query = query.filter(Material.category_id == category_id)
        
        # 关键词搜索（物料名称、编码）
        if keyword:
            query = query.filter(
                or_(
                    Material.name.like(f'%{keyword}%'),
                    Material.code.like(f'%{keyword}%')
                )
            )
        
        # 按存放位置筛选
        if location:
            query = query.filter(Material.location.like(f'%{location}%'))
        
        # 按物料名称排序
        query = query.order_by(Material.name.asc())
        
        # 分页查询
        total = query.count()
        materials = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式并按状态筛选
        data = []
        for material in materials:
            material_dict = material.to_dict()
            if not status or material_dict['status'] == status:
                data.append(material_dict)
        
        # 如果有状态筛选，重新计算总数
        if status:
            total = len(data)
        
        return api_paginated_success(data, page, limit, total, "获取物料列表成功")
        
    except Exception as e:
        return api_error(f"获取物料列表失败: {str(e)}", 500)

@api_bp.route('/materials', methods=['POST'])
@jwt_required()
def create_material():
    """创建物料"""
    try:
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['code', 'name', 'category_id', 'unit']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"{field}不能为空", 400)
        
        # 验证分类是否存在
        category = MaterialCategory.query.get(data['category_id'])
        if not category:
            return api_error("物料分类不存在", 400)
        
        # 检查物料编码是否已存在
        existing_material = Material.query.filter_by(code=data['code']).first()
        if existing_material:
            return api_error("物料编码已存在", 400)
        
        # 创建新物料
        material = Material(
            code=data['code'],
            name=data['name'],
            category_id=data['category_id'],
            description=data.get('description'),
            unit=data['unit'],
            stock_quantity=data.get('stock_quantity', 0),
            min_stock=data.get('min_stock'),
            max_stock=data.get('max_stock'),
            unit_price=data.get('unit_price'),
            location=data.get('location'),
            supplier=data.get('supplier')
        )
        
        db.session.add(material)
        db.session.commit()
        
        return api_success(data=material.to_dict(), message="创建物料成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建物料失败: {str(e)}", 500)

@api_bp.route('/materials/<int:material_id>', methods=['GET'])
@jwt_required()
def get_material_detail(material_id):
    """获取物料详情"""
    try:
        material = Material.query.get(material_id)
        
        if not material:
            return api_error("物料不存在", 404)
        
        return api_success(data=material.to_dict(), message="获取物料详情成功")
        
    except Exception as e:
        return api_error(f"获取物料详情失败: {str(e)}", 500)

@api_bp.route('/materials/<int:material_id>', methods=['PUT'])
@jwt_required()
def update_material(material_id):
    """更新物料"""
    try:
        material = Material.query.get(material_id)
        
        if not material:
            return api_error("物料不存在", 404)
        
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 检查物料编码是否已存在（排除当前物料）
        if 'code' in data and data['code'] != material.code:
            existing_material = Material.query.filter(
                Material.code == data['code'],
                Material.id != material_id
            ).first()
            
            if existing_material:
                return api_error("物料编码已存在", 400)
        
        # 验证分类是否存在
        if 'category_id' in data:
            category = MaterialCategory.query.get(data['category_id'])
            if not category:
                return api_error("物料分类不存在", 400)
        
        # 更新字段
        for field in ['code', 'name', 'category_id', 'description', 'unit', 
                     'stock_quantity', 'min_stock', 'max_stock', 'unit_price', 
                     'location', 'supplier']:
            if field in data:
                setattr(material, field, data[field])
        
        db.session.commit()
        
        return api_success(data=material.to_dict(), message="更新物料成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"更新物料失败: {str(e)}", 500)

@api_bp.route('/materials/batch-update-stock', methods=['PUT'])
@jwt_required()
def batch_update_material_stock():
    """批量更新物料库存"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('updates'):
            return api_error("更新数据不能为空", 400)
        
        updates = data['updates']
        if not isinstance(updates, list) or len(updates) == 0:
            return api_error("更新列表不能为空", 400)
        
        results = []
        updated_count = 0
        failed_count = 0
        
        for update in updates:
            material_id = update.get('material_id')
            stock_quantity = update.get('stock_quantity')
            notes = update.get('notes', '')
            
            if not material_id or stock_quantity is None:
                results.append({
                    'material_id': material_id,
                    'success': False,
                    'message': '物料ID和库存数量不能为空'
                })
                failed_count += 1
                continue
            
            try:
                material = Material.query.get(material_id)
                if not material:
                    results.append({
                        'material_id': material_id,
                        'success': False,
                        'message': '物料不存在'
                    })
                    failed_count += 1
                    continue
                
                # 记录库存变更前的数量
                before_quantity = material.stock_quantity
                
                # 更新库存
                material.stock_quantity = stock_quantity
                
                # 创建库存变更记录
                transaction = MaterialTransaction(
                    material_id=material_id,
                    transaction_type='adjust',
                    quantity=stock_quantity - before_quantity,
                    before_quantity=before_quantity,
                    after_quantity=stock_quantity,
                    user_id=current_user_id,
                    notes=f"批量库存调整: {notes}"
                )
                
                db.session.add(transaction)
                
                results.append({
                    'material_id': material_id,
                    'success': True,
                    'message': '更新成功'
                })
                updated_count += 1
                
            except Exception as e:
                results.append({
                    'material_id': material_id,
                    'success': False,
                    'message': f'更新失败: {str(e)}'
                })
                failed_count += 1
        
        db.session.commit()
        
        return api_success(
            data={
                'updated_count': updated_count,
                'failed_count': failed_count,
                'results': results
            },
            message=f"批量更新完成，成功{updated_count}条，失败{failed_count}条"
        )
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"批量更新物料库存失败: {str(e)}", 500)

@api_bp.route('/materials/<int:material_id>', methods=['DELETE'])
@jwt_required()
def delete_material(material_id):
    """删除物料"""
    try:
        material = Material.query.get(material_id)
        
        if not material:
            return api_error("物料不存在", 404)
        
        # 检查是否有相关的申领记录或交易记录
        transactions_count = MaterialTransaction.query.filter_by(material_id=material_id).count()
        if transactions_count > 0:
            return api_error(f"该物料有{transactions_count}条交易记录，无法删除", 400)
        
        db.session.delete(material)
        db.session.commit()
        
        return api_success(message="删除物料成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"删除物料失败: {str(e)}", 500)

# 物料申领相关接口
@api_bp.route('/material-requests', methods=['POST'])
@jwt_required()
def create_material_request():
    """创建物料申领"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return api_error("请求数据不能为空", 400)
        
        # 验证必填字段
        required_fields = ['materials']
        for field in required_fields:
            if not data.get(field):
                return api_error(f"{field}不能为空", 400)
        
        # 验证申领物料列表
        materials = data['materials']
        if not isinstance(materials, list) or len(materials) == 0:
            return api_error("申领物料列表不能为空", 400)
        
        # 验证每个物料是否存在
        for item in materials:
            if not item.get('material_id') or not item.get('quantity'):
                return api_error("物料ID和数量不能为空", 400)
            
            material = Material.query.get(item['material_id'])
            if not material:
                return api_error(f"物料ID {item['material_id']} 不存在", 400)
        
        # 生成申领单号
        today = date.today()
        request_number = f"REQ{today.strftime('%Y%m%d')}{MaterialRequest.query.filter(MaterialRequest.created_at >= today).count() + 1:04d}"
        
        # 解析预期归还日期
        expected_return_date = None
        if data.get('expected_return_date'):
            try:
                expected_return_date = datetime.strptime(data['expected_return_date'], '%Y-%m-%d').date()
            except ValueError:
                return api_error("预期归还日期格式错误，应为YYYY-MM-DD", 400)
        
        # 创建申领记录
        material_request = MaterialRequest(
            request_number=request_number,
            user_id=current_user_id,
            project_name=data.get('project_name'),
            materials=materials,
            expected_return_date=expected_return_date,
            notes=data.get('notes')
        )
        
        db.session.add(material_request)
        db.session.commit()
        
        return api_success(data=material_request.to_dict(), message="物料申领申请创建成功", code=201)
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"创建物料申领失败: {str(e)}", 500)

@api_bp.route('/material-requests', methods=['GET'])
@jwt_required()
def get_material_requests():
    """获取物料申领列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status')
        user_id = request.args.get('user_id', type=int)
        
        # 构建查询
        query = MaterialRequest.query
        
        # 按状态筛选
        if status:
            query = query.filter(MaterialRequest.status == status)
        
        # 按用户筛选
        if user_id:
            query = query.filter(MaterialRequest.user_id == user_id)
        
        # 按创建时间倒序排序
        query = query.order_by(MaterialRequest.created_at.desc())
        
        # 分页查询
        total = query.count()
        requests = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [request.to_dict() for request in requests]
        
        return api_paginated_success(data, page, limit, total, "获取物料申领列表成功")
        
    except Exception as e:
        return api_error(f"获取物料申领列表失败: {str(e)}", 500)

@api_bp.route('/material-requests/<int:request_id>/approve', methods=['PUT'])
@jwt_required()
def approve_material_request(request_id):
    """审批物料申领"""
    try:
        current_user_id = get_jwt_identity()
        material_request = MaterialRequest.query.get(request_id)
        
        if not material_request:
            return api_error("申领记录不存在", 404)
        
        if material_request.status != 'pending':
            return api_error("只能审批待审核状态的申领", 400)
        
        data = request.get_json()
        
        if not data or not data.get('action'):
            return api_error("审批动作不能为空", 400)
        
        action = data['action']
        if action not in ['approve', 'reject']:
            return api_error("无效的审批动作", 400)
        
        # 更新审批信息
        material_request.approver_id = current_user_id
        material_request.approved_at = beijing_now()
        material_request.approval_comment = data.get('comment')
        
        if action == 'approve':
            material_request.status = 'approved'
            material_request.approved_materials = data.get('approved_materials', material_request.materials)
        else:
            material_request.status = 'rejected'
        
        db.session.commit()
        
        return api_success(data=material_request.to_dict(), message=f"申领{'批准' if action == 'approve' else '拒绝'}成功")
        
    except Exception as e:
        db.session.rollback()
        return api_error(f"审批物料申领失败: {str(e)}", 500)

# 物料出入库记录相关接口
@api_bp.route('/material-transactions', methods=['GET'])
@jwt_required()
def get_material_transactions():
    """获取物料出入库记录"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        material_id = request.args.get('material_id', type=int)
        transaction_type = request.args.get('transaction_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 构建查询
        query = MaterialTransaction.query
        
        # 按物料筛选
        if material_id:
            query = query.filter(MaterialTransaction.material_id == material_id)
        
        # 按交易类型筛选
        if transaction_type:
            query = query.filter(MaterialTransaction.transaction_type == transaction_type)
        
        # 按日期范围筛选
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(MaterialTransaction.created_at >= start_dt)
            except ValueError:
                return api_error("开始日期格式错误，应为YYYY-MM-DD", 400)
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                # 包含结束日期的整天
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(MaterialTransaction.created_at <= end_dt)
            except ValueError:
                return api_error("结束日期格式错误，应为YYYY-MM-DD", 400)
        
        # 按创建时间倒序排序
        query = query.order_by(MaterialTransaction.created_at.desc())
        
        # 分页查询
        total = query.count()
        transactions = query.offset((page - 1) * limit).limit(limit).all()
        
        # 转换为字典格式
        data = [transaction.to_dict() for transaction in transactions]
        
        return api_paginated_success(data, page, limit, total, "获取物料出入库记录成功")
        
    except Exception as e:
        return api_error(f"获取物料出入库记录失败: {str(e)}", 500)

# 库存统计相关接口
@api_bp.route('/materials/statistics', methods=['GET'])
@jwt_required()
def get_material_statistics():
    """获取库存统计"""
    try:
        period = request.args.get('period', 'month')
        category_id = request.args.get('category_id', type=int)
        
        # 基础统计
        query = Material.query
        if category_id:
            query = query.filter(Material.category_id == category_id)
        
        materials = query.all()
        
        total_materials = len(materials)
        total_value = sum(float(m.unit_price or 0) * m.stock_quantity for m in materials)
        low_stock_count = sum(1 for m in materials if m.status == 'low_stock')
        out_of_stock_count = sum(1 for m in materials if m.status == 'out_of_stock')
        
        # 出库统计
        now = datetime.now()
        if period == 'day':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now.weekday())
        else:  # month
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        out_transactions = MaterialTransaction.query.filter(
            MaterialTransaction.transaction_type == 'out',
            MaterialTransaction.created_at >= start_time
        )
        
        if category_id:
            out_transactions = out_transactions.join(Material).filter(Material.category_id == category_id)
        
        period_out = sum(t.quantity for t in out_transactions.all())
        
        # 热门申领物料
        top_requested = db.session.query(
            Material.id,
            Material.name,
            func.count(MaterialTransaction.id).label('request_count')
        ).join(MaterialTransaction).filter(
            MaterialTransaction.transaction_type == 'out'
        ).group_by(Material.id, Material.name).order_by(
            func.count(MaterialTransaction.id).desc()
        ).limit(5).all()
        
        top_requested_materials = [
            {
                'material_id': item.id,
                'material_name': item.name,
                'request_count': item.request_count
            }
            for item in top_requested
        ]
        
        # 分类分布
        category_stats = db.session.query(
            MaterialCategory.id,
            MaterialCategory.name,
            func.count(Material.id).label('material_count'),
            func.sum(Material.stock_quantity * func.coalesce(Material.unit_price, 0)).label('total_value')
        ).join(Material).group_by(
            MaterialCategory.id, MaterialCategory.name
        ).all()
        
        category_distribution = [
            {
                'category_id': item.id,
                'category_name': item.name,
                'material_count': item.material_count,
                'total_value': float(item.total_value or 0)
            }
            for item in category_stats
        ]
        
        data = {
            'total_materials': total_materials,
            'total_value': total_value,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            f'{period}_out': period_out,
            'top_requested_materials': top_requested_materials,
            'category_distribution': category_distribution
        }
        
        return api_success(data=data, message="获取库存统计成功")
        
    except Exception as e:
        return api_error(f"获取库存统计失败: {str(e)}", 500)