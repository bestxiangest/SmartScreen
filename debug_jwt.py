#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JWT调试脚本 - 诊断JWT配置问题
"""

import sys
import os
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
import jwt as pyjwt

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_jwt_configuration():
    """测试JWT配置"""
    print("=== JWT配置诊断 ===")
    print(f"Python版本: {sys.version}")
    
    # 检查依赖包版本
    try:
        import flask_jwt_extended
        print(f"Flask-JWT-Extended版本: {flask_jwt_extended.__version__}")
    except Exception as e:
        print(f"Flask-JWT-Extended导入错误: {e}")
    
    try:
        print(f"PyJWT版本: {pyjwt.__version__}")
    except Exception as e:
        print(f"PyJWT版本获取错误: {e}")
    
    # 创建测试Flask应用
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['JWT_SECRET_KEY'] = 'jwt-test-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # 测试不同的JWT算法配置
    algorithms_to_test = ['HS256', 'HS384', 'HS512']
    
    for algorithm in algorithms_to_test:
        print(f"\n--- 测试算法: {algorithm} ---")
        
        # 设置JWT算法
        app.config['JWT_ALGORITHM'] = algorithm
        
        jwt_manager = JWTManager(app)
        
        with app.app_context():
            try:
                # 尝试创建JWT令牌
                token = create_access_token(
                    identity='test_user_123',
                    expires_delta=timedelta(hours=24)
                )
                print(f"✓ 成功创建JWT令牌 (算法: {algorithm})")
                print(f"  令牌前50字符: {token[:50]}...")
                
                # 尝试解码令牌
                try:
                    decoded = pyjwt.decode(
                        token, 
                        app.config['JWT_SECRET_KEY'], 
                        algorithms=[algorithm]
                    )
                    print(f"✓ 成功解码JWT令牌")
                    print(f"  用户ID: {decoded.get('sub')}")
                except Exception as decode_error:
                    print(f"✗ JWT令牌解码失败: {decode_error}")
                    
            except Exception as create_error:
                print(f"✗ JWT令牌创建失败: {create_error}")
                print(f"  错误类型: {type(create_error).__name__}")
                if 'digestmod' in str(create_error):
                    print(f"  ⚠️  检测到digestmod错误，这通常与HMAC算法配置有关")

def test_hmac_compatibility():
    """测试HMAC兼容性"""
    print("\n=== HMAC兼容性测试 ===")
    
    try:
        import hmac
        import hashlib
        
        # 测试不同的HMAC配置
        secret = b'test-secret-key'
        message = b'test-message'
        
        # 测试默认配置
        try:
            # 新版本的hmac.new需要digestmod参数
            digest1 = hmac.new(secret, message, hashlib.sha256).hexdigest()
            print(f"✓ HMAC SHA256 (显式digestmod): {digest1[:20]}...")
        except Exception as e:
            print(f"✗ HMAC SHA256 (显式digestmod)失败: {e}")
        
        # 测试不指定digestmod（可能在旧版本中工作）
        try:
            digest2 = hmac.new(secret, message).hexdigest()
            print(f"✓ HMAC (默认digestmod): {digest2[:20]}...")
        except Exception as e:
            print(f"✗ HMAC (默认digestmod)失败: {e}")
            print(f"  这可能是问题的根源！")
            
    except Exception as e:
        print(f"HMAC测试失败: {e}")

def test_werkzeug_compatibility():
    """测试Werkzeug兼容性"""
    print("\n=== Werkzeug兼容性测试 ===")
    
    try:
        from werkzeug.security import generate_password_hash, check_password_hash
        import werkzeug
        
        print(f"Werkzeug版本: {werkzeug.__version__}")
        
        # 测试密码哈希
        test_password = 'test123'
        
        # 测试scrypt方法
        try:
            hash_scrypt = generate_password_hash(test_password, method='scrypt')
            verify_scrypt = check_password_hash(hash_scrypt, test_password)
            print(f"✓ Scrypt哈希: {hash_scrypt[:30]}... (验证: {verify_scrypt})")
        except Exception as e:
            print(f"✗ Scrypt哈希失败: {e}")
        
        # 测试pbkdf2方法
        try:
            hash_pbkdf2 = generate_password_hash(test_password, method='pbkdf2:sha256')
            verify_pbkdf2 = check_password_hash(hash_pbkdf2, test_password)
            print(f"✓ PBKDF2哈希: {hash_pbkdf2[:30]}... (验证: {verify_pbkdf2})")
        except Exception as e:
            print(f"✗ PBKDF2哈希失败: {e}")
            
    except Exception as e:
        print(f"Werkzeug测试失败: {e}")

def main():
    """主函数"""
    print("智慧实验室电子班牌系统 - JWT问题诊断工具")
    print("=" * 60)
    
    test_jwt_configuration()
    test_hmac_compatibility()
    test_werkzeug_compatibility()
    
    print("\n=== 诊断建议 ===")
    print("1. 如果看到'digestmod'错误，可能需要：")
    print("   - 升级PyJWT到最新版本")
    print("   - 在JWT配置中显式指定算法")
    print("   - 检查Python版本兼容性")
    print("2. 如果Werkzeug有警告，确保使用scrypt方法")
    print("3. 检查服务器和本地环境的Python/包版本差异")

if __name__ == '__main__':
    main()