#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db
from app.models import User
from flask import Flask

# 创建Flask应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zzn20041031@localhost:3306/smartscreen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # 查找包含"陈都"的用户
    users = User.query.filter(User.full_name.like('%陈都%')).all()
    print('找到的用户:')
    for u in users:
        print(f'ID: {u.id}, 用户名: {u.username}, 姓名: "{u.full_name}", 长度: {len(u.full_name)}')
        # 检查是否有不可见字符
        print(f'姓名的字节表示: {repr(u.full_name)}')
        print('---')
    
    if not users:
        print('没有找到包含"陈都"的用户')
        # 显示所有用户
        all_users = User.query.all()
        print(f'\n数据库中共有 {len(all_users)} 个用户:')
        for u in all_users:
            print(f'ID: {u.id}, 用户名: {u.username}, 姓名: "{u.full_name}"')