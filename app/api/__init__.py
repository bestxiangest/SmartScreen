#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - API蓝图包
"""

from flask import Blueprint

# 创建API蓝图
api_bp = Blueprint('api', __name__)

# 导入所有API模块
from . import auth
from . import announcements
from . import projects
from . import schedules
from . import devices
from . import attendance
from . import labs
from . import safety
from . import ai_training
from . import environmental
from . import upload
from . import users