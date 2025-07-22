#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 应用启动文件
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # 从环境变量获取配置，默认为开发环境
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app.run(debug=debug, host=host, port=port)