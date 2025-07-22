#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 批量用户注册程序
"""

import os
import sys
import csv
import pandas as pd
from datetime import datetime
from flask import Flask
from werkzeug.security import generate_password_hash

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 创建Flask应用上下文
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zzn20041031@localhost:3306/smartscreen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
from app import db
from app.models import User
db.init_app(app)

class BatchUserRegistration:
    """批量用户注册类"""
    
    def __init__(self):
        self.app = app
        self.success_count = 0
        self.error_count = 0
        self.errors = []
    
    def validate_user_data(self, user_data):
        """验证用户数据"""
        required_fields = ['username', 'password', 'full_name']
        errors = []
        
        # 检查必填字段
        for field in required_fields:
            if not user_data.get(field) or str(user_data[field]).strip() == '':
                errors.append(f"缺少必填字段: {field}")
        
        # 验证用户名长度
        if user_data.get('username') and len(str(user_data['username'])) > 50:
            errors.append("用户名长度不能超过50个字符")
        
        # 验证真实姓名长度
        if user_data.get('full_name') and len(str(user_data['full_name'])) > 100:
            errors.append("真实姓名长度不能超过100个字符")
        
        # 验证邮箱格式（如果提供）
        if user_data.get('email'):
            email = str(user_data['email']).strip()
            if email and '@' not in email:
                errors.append("邮箱格式不正确")
            if len(email) > 100:
                errors.append("邮箱长度不能超过100个字符")
        
        # 验证手机号长度（如果提供）
        if user_data.get('phone_number'):
            phone = str(user_data['phone_number']).strip()
            if len(phone) > 20:
                errors.append("手机号长度不能超过20个字符")
        
        return errors
    
    def check_user_exists(self, username):
        """检查用户是否已存在"""
        return User.query.filter_by(username=username).first() is not None
    
    def create_user(self, user_data):
        """创建单个用户"""
        try:
            # 验证数据
            validation_errors = self.validate_user_data(user_data)
            if validation_errors:
                return False, f"数据验证失败: {'; '.join(validation_errors)}"
            
            username = str(user_data['username']).strip()
            
            # 检查用户是否已存在
            if self.check_user_exists(username):
                return False, f"用户名 '{username}' 已存在"
            
            # 创建用户对象
            user = User(
                username=username,
                full_name=str(user_data['full_name']).strip(),
                email=str(user_data.get('email', '')).strip() or None,
                phone_number=str(user_data.get('phone_number', '')).strip() or None
            )
            
            # 设置密码
            user.set_password(str(user_data['password']))
            
            # 保存到数据库
            db.session.add(user)
            db.session.commit()
            
            return True, f"用户 '{username}' 创建成功"
            
        except Exception as e:
            db.session.rollback()
            return False, f"创建用户失败: {str(e)}"
    
    def register_from_csv(self, csv_file_path):
        """从CSV文件批量注册用户"""
        print(f"\n开始从CSV文件批量注册用户: {csv_file_path}")
        print("=" * 60)
        
        try:
            # 读取CSV文件
            df = pd.read_csv(csv_file_path, encoding='utf-8')
            
            # 检查必要的列
            required_columns = ['username', 'password', 'full_name']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"错误: CSV文件缺少必要的列: {missing_columns}")
                return
            
            print(f"找到 {len(df)} 条用户记录")
            print("\n开始注册...")
            
            with self.app.app_context():
                for index, row in df.iterrows():
                    user_data = row.to_dict()
                    success, message = self.create_user(user_data)
                    
                    if success:
                        self.success_count += 1
                        print(f"✓ 第{index+1}行: {message}")
                    else:
                        self.error_count += 1
                        error_msg = f"第{index+1}行: {message}"
                        self.errors.append(error_msg)
                        print(f"✗ {error_msg}")
            
        except FileNotFoundError:
            print(f"错误: 找不到文件 {csv_file_path}")
        except Exception as e:
            print(f"读取CSV文件时发生错误: {str(e)}")
    
    def register_interactive(self):
        """交互式批量注册用户"""
        print("\n交互式批量用户注册")
        print("=" * 40)
        print("输入用户信息，按回车继续下一个用户，输入 'quit' 结束")
        print("必填字段: 用户名、密码、真实姓名")
        print("可选字段: 邮箱、手机号")
        print()
        
        with self.app.app_context():
            while True:
                print(f"\n--- 用户 #{self.success_count + self.error_count + 1} ---")
                
                # 获取用户输入
                username = input("用户名: ").strip()
                if username.lower() == 'quit':
                    break
                
                password = input("密码: ").strip()
                if password.lower() == 'quit':
                    break
                
                full_name = input("真实姓名: ").strip()
                if full_name.lower() == 'quit':
                    break
                
                email = input("邮箱 (可选): ").strip()
                if email.lower() == 'quit':
                    break
                
                phone_number = input("手机号 (可选): ").strip()
                if phone_number.lower() == 'quit':
                    break
                
                # 构建用户数据
                user_data = {
                    'username': username,
                    'password': password,
                    'full_name': full_name,
                    'email': email if email else None,
                    'phone_number': phone_number if phone_number else None
                }
                
                # 创建用户
                success, message = self.create_user(user_data)
                
                if success:
                    self.success_count += 1
                    print(f"✓ {message}")
                else:
                    self.error_count += 1
                    self.errors.append(message)
                    print(f"✗ {message}")
    
    def generate_sample_csv(self, file_path="sample_users.csv"):
        """生成示例CSV文件"""
        sample_data = [
            {
                'username': 'student001',
                'password': 'password123',
                'full_name': '张三',
                'email': 'zhangsan@example.com',
                'phone_number': '13800138001'
            },
            {
                'username': 'student002',
                'password': 'password123',
                'full_name': '李四',
                'email': 'lisi@example.com',
                'phone_number': '13800138002'
            },
            {
                'username': 'teacher001',
                'password': 'teacher123',
                'full_name': '王老师',
                'email': 'wangteacher@example.com',
                'phone_number': '13800138003'
            }
        ]
        
        df = pd.DataFrame(sample_data)
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"示例CSV文件已生成: {file_path}")
        print("CSV文件格式:")
        print("username,password,full_name,email,phone_number")
        print("student001,password123,张三,zhangsan@example.com,13800138001")
    
    def print_summary(self):
        """打印注册结果摘要"""
        print("\n" + "=" * 60)
        print("批量注册结果摘要")
        print("=" * 60)
        print(f"成功注册: {self.success_count} 个用户")
        print(f"注册失败: {self.error_count} 个用户")
        print(f"总计处理: {self.success_count + self.error_count} 个用户")
        
        if self.errors:
            print("\n失败详情:")
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. {error}")
        
        print("\n注册完成!")

def main():
    """主函数"""
    print("智慧实验室电子班牌系统 - 批量用户注册程序")
    print("=" * 60)
    
    registrar = BatchUserRegistration()
    
    while True:
        print("\n请选择操作:")
        print("1. 从CSV文件批量注册")
        print("2. 交互式批量注册")
        print("3. 生成示例CSV文件")
        print("4. 退出")
        
        choice = input("\n请输入选项 (1-4): ").strip()
        
        if choice == '1':
            csv_file = input("请输入CSV文件路径: ").strip()
            if csv_file:
                registrar.register_from_csv(csv_file)
                registrar.print_summary()
        
        elif choice == '2':
            registrar.register_interactive()
            registrar.print_summary()
        
        elif choice == '3':
            file_path = input("请输入生成的CSV文件名 (默认: sample_users.csv): ").strip()
            if not file_path:
                file_path = "sample_users.csv"
            registrar.generate_sample_csv(file_path)
        
        elif choice == '4':
            print("\n感谢使用批量用户注册程序!")
            break
        
        else:
            print("无效选项，请重新选择")

if __name__ == '__main__':
    main()