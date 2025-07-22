#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JWT HMAC修复脚本
解决Flask-JWT-Extended在某些环境下的digestmod问题
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def patch_jwt_hmac():
    """
    修复JWT HMAC digestmod问题
    这个补丁确保HMAC调用时总是包含digestmod参数
    """
    try:
        import hmac
        import hashlib
        
        # 保存原始的hmac.new函数
        original_hmac_new = hmac.new
        
        def patched_hmac_new(key, msg=None, digestmod=None):
            """
            修复后的hmac.new函数，确保总是有digestmod参数
            """
            if digestmod is None:
                # 如果没有指定digestmod，默认使用sha256
                digestmod = hashlib.sha256
            
            return original_hmac_new(key, msg, digestmod)
        
        # 替换hmac.new函数
        hmac.new = patched_hmac_new
        
        print("✓ JWT HMAC补丁已应用")
        return True
        
    except Exception as e:
        print(f"✗ JWT HMAC补丁应用失败: {e}")
        return False

def test_jwt_after_patch():
    """
    测试补丁后的JWT功能
    """
    try:
        from flask import Flask
        from flask_jwt_extended import JWTManager, create_access_token
        from datetime import timedelta
        
        # 创建测试应用
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test-secret'
        app.config['JWT_SECRET_KEY'] = 'jwt-test-secret'
        app.config['JWT_ALGORITHM'] = 'HS256'
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
        
        jwt = JWTManager(app)
        
        with app.app_context():
            # 尝试创建JWT令牌
            token = create_access_token(
                identity='test_user',
                expires_delta=timedelta(hours=24)
            )
            
            print(f"✓ JWT令牌创建成功: {token[:50]}...")
            return True
            
    except Exception as e:
        print(f"✗ JWT测试失败: {e}")
        return False

def main():
    """
    主函数
    """
    print("智慧实验室电子班牌系统 - JWT HMAC修复工具")
    print("=" * 50)
    
    # 应用补丁
    if patch_jwt_hmac():
        # 测试补丁效果
        if test_jwt_after_patch():
            print("\n✓ JWT HMAC问题已修复，可以正常使用")
        else:
            print("\n✗ 补丁应用后仍有问题")
    else:
        print("\n✗ 无法应用JWT HMAC补丁")
    
    print("\n=== 使用说明 ===")
    print("1. 将此补丁代码添加到应用启动时执行")
    print("2. 或者在app/__init__.py中导入并调用patch_jwt_hmac()")
    print("3. 确保在导入Flask-JWT-Extended之前应用补丁")

if __name__ == '__main__':
    main()