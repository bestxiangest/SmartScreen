#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 扩展模块
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# 创建扩展实例
db = SQLAlchemy()
jwt = JWTManager()