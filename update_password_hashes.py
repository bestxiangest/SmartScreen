#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新用户密码哈希格式脚本
用于将现有的bcrypt密码哈希更新为scrypt格式
"""

import os
import sys
from werkzeug.security import generate_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 创建Flask应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zzn20041031@localhost:3306/smartscreen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 定义User模型
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    face_data = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime)

def update_password_hashes():
    """更新所有用户的密码哈希格式"""
    with app.app_context():
        try:
            # 获取所有用户
            users = User.query.all()
            
            if not users:
                print("数据库中没有用户")
                return
            
            print(f"找到 {len(users)} 个用户，开始更新密码哈希格式...")
            
            # 默认密码映射（基于mysql.sql中的数据）
            default_passwords = {
                'admin': 'admin123',
                '2024001': 'teacher123',  # 黄老师
                '2024101': 'student123',  # 吴文静
                '2024102': 'student123',  # 黄旺
                '2024103': 'student123',  # 朱海月
                '2024104': 'student123',  # 张祖宁
            }
            
            updated_count = 0
            
            for user in users:
                # 检查是否是旧的bcrypt格式
                if user.password_hash.startswith('$2a$') or user.password_hash.startswith('$2b$'):
                    # 获取默认密码
                    default_password = default_passwords.get(user.username, 'password123')
                    
                    print(f"更新用户 {user.username} ({user.full_name}) 的密码哈希...")
                    
                    # 使用scrypt方法重新生成密码哈希
                    user.password_hash = generate_password_hash(default_password, method='scrypt')
                    updated_count += 1
                    
                    print(f"  用户名: {user.username}")
                    print(f"  默认密码: {default_password}")
                    print(f"  新哈希: {user.password_hash[:50]}...")
                else:
                    print(f"用户 {user.username} 的密码哈希已经是新格式，跳过")
            
            if updated_count > 0:
                # 提交更改
                db.session.commit()
                print(f"\n成功更新了 {updated_count} 个用户的密码哈希格式")
                
                print("\n=== 更新后的用户登录信息 ===")
                for username, password in default_passwords.items():
                    user = User.query.filter_by(username=username).first()
                    if user:
                        print(f"用户名: {username}, 密码: {password}")
            else:
                print("\n没有需要更新的用户")
                
        except Exception as e:
            db.session.rollback()
            print(f"更新密码哈希失败: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    print("智慧实验室电子班牌系统 - 密码哈希格式更新工具")
    print("=" * 50)
    print("此工具将把现有的bcrypt密码哈希更新为scrypt格式")
    print("注意: 这将重置所有用户的密码为默认密码")
    print()
    
    confirm = input("确认要继续吗？(y/N): ").lower().strip()
    if confirm != 'y':
        print("操作已取消")
        return
    
    update_password_hashes()

if __name__ == '__main__':
    main()