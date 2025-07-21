#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建管理员账户脚本
"""

import os
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app, db
    from app.models import User, Role, UserRole
except ImportError:
    print("错误: 无法导入应用模块，请确保在项目根目录运行此脚本")
    sys.exit(1)

def create_admin_user():
    """创建管理员用户"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已存在管理员用户
            existing_admin = User.query.filter_by(username='admin').first()
            if existing_admin:
                print("管理员用户已存在！")
                print(f"用户名: {existing_admin.username}")
                print(f"真实姓名: {existing_admin.real_name}")
                print(f"创建时间: {existing_admin.created_at}")
                
                # 询问是否重置密码
                reset = input("是否重置管理员密码？(y/N): ").lower().strip()
                if reset == 'y':
                    new_password = input("请输入新密码 (默认: admin123): ").strip() or 'admin123'
                    existing_admin.password_hash = generate_password_hash(new_password)
                    db.session.commit()
                    print(f"管理员密码已重置为: {new_password}")
                return
            
            # 创建管理员角色（如果不存在）
            admin_role = Role.query.filter_by(role_name='管理员').first()
            if not admin_role:
                admin_role = Role(
                    role_name='管理员',
                    permissions=['all']  # 使用JSON格式
                )
                db.session.add(admin_role)
                db.session.flush()  # 获取角色ID
                print("已创建管理员角色")
            
            # 获取管理员信息
            print("=== 创建管理员账户 ===")
            username = input("请输入管理员用户名 (默认: admin): ").strip() or 'admin'
            password = input("请输入管理员密码 (默认: admin123): ").strip() or 'admin123'
            real_name = input("请输入管理员真实姓名 (默认: 系统管理员): ").strip() or '系统管理员'
            email = input("请输入管理员邮箱 (可选): ").strip() or None
            phone = input("请输入管理员电话 (可选): ").strip() or None
            
            # 检查用户名是否已存在
            if User.query.filter_by(username=username).first():
                print(f"错误: 用户名 '{username}' 已存在！")
                return
            
            # 创建管理员用户
            admin_user = User(
                username=username,
                password_hash=generate_password_hash(password),
                full_name=real_name,
                email=email,
                phone_number=phone  # 使用正确的字段名phone_number
            )
            
            db.session.add(admin_user)
            db.session.flush()  # 获取用户ID
            
            # 分配管理员角色
            user_role = UserRole(
                user_id=admin_user.id,  # 使用正确的字段名
                role_id=admin_role.id   # 使用正确的字段名
            )
            db.session.add(user_role)
            
            # 提交事务
            db.session.commit()
            
            print("\n=== 管理员账户创建成功！ ===")
            print(f"用户名: {username}")
            print(f"密码: {password}")
            print(f"真实姓名: {real_name}")
            print(f"邮箱: {email or '未设置'}")
            print(f"角色: 管理员")
            print("\n请妥善保管登录信息！")
            
        except Exception as e:
            db.session.rollback()
            print(f"创建管理员账户失败: {str(e)}")
            import traceback
            traceback.print_exc()

def create_sample_roles():
    """创建示例角色"""
    app = create_app()
    
    with app.app_context():
        try:
            # 定义角色数据
            roles_data = [
                {
                    'role_name': '管理员',
                    'permissions': ['all']
                },
                {
                    'role_name': '教师',
                    'permissions': ['courses', 'students', 'announcements']
                },
                {
                    'role_name': '学生',
                    'permissions': ['view_courses', 'attendance']
                },
                {
                    'role_name': '实验室管理员',
                    'permissions': ['devices', 'safety', 'environment']
                }
            ]
            
            created_count = 0
            for role_data in roles_data:
                # 检查角色是否已存在
                existing_role = Role.query.filter_by(role_name=role_data['role_name']).first()
                if not existing_role:
                    role = Role(**role_data)
                    db.session.add(role)
                    created_count += 1
                    print(f"创建角色: {role_data['role_name']}")
                else:
                    print(f"角色已存在: {role_data['role_name']}")
            
            if created_count > 0:
                db.session.commit()
                print(f"\n成功创建 {created_count} 个角色")
            else:
                print("\n所有角色都已存在")
                
        except Exception as e:
            db.session.rollback()
            print(f"创建角色失败: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    print("智慧实验室电子班牌系统 - 管理员账户创建工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 创建管理员账户")
        print("2. 创建示例角色")
        print("3. 退出")
        
        choice = input("\n请输入选项 (1-3): ").strip()
        
        if choice == '1':
            create_admin_user()
        elif choice == '2':
            create_sample_roles()
        elif choice == '3':
            print("再见！")
            break
        else:
            print("无效选项，请重新选择")

if __name__ == '__main__':
    main()