#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 统一响应格式
"""

from flask import jsonify

def api_success(data=None, message="操作成功", code=200):
    """成功响应格式
    
    Args:
        data: 响应数据
        message: 响应消息
        code: HTTP状态码
    
    Returns:
        Flask Response对象
    """
    response = {
        "code": code,
        "message": message,
        "success": True
    }
    
    if data is not None:
        response["data"] = data
    
    return jsonify(response), code

def api_error(message="操作失败", error_code=400, details=None):
    """错误响应格式
    
    Args:
        message: 错误消息
        error_code: HTTP错误状态码
        details: 详细错误信息
    
    Returns:
        Flask Response对象
    """
    response = {
        "code": error_code,
        "message": message,
        "success": False
    }
    
    if details is not None:
        response["details"] = details
    
    return jsonify(response), error_code

def api_paginated_success(data, page, limit, total, message="获取成功"):
    """分页成功响应格式
    
    Args:
        data: 分页数据列表
        page: 当前页码
        limit: 每页数量
        total: 总记录数
        message: 响应消息
    
    Returns:
        Flask Response对象
    """
    total_pages = (total + limit - 1) // limit  # 向上取整
    
    response_data = {
        "items": data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }
    
    return api_success(data=response_data, message=message)

def format_validation_error(errors):
    """格式化表单验证错误
    
    Args:
        errors: 验证错误字典
    
    Returns:
        格式化后的错误信息
    """
    error_messages = []
    for field, messages in errors.items():
        if isinstance(messages, list):
            error_messages.extend([f"{field}: {msg}" for msg in messages])
        else:
            error_messages.append(f"{field}: {messages}")
    
    return "; ".join(error_messages)