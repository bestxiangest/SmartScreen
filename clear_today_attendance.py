#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db
from app.models import AttendanceLog, User
from flask import Flask
from datetime import date

# 创建Flask应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zzn20041031@localhost:3306/smartscreen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # 查找陈都的用户ID
    user = User.query.filter_by(full_name='陈都').first()
    if user:
        print(f"找到用户: ID={user.id}, 姓名='{user.full_name}'")
        
        # 删除今天的签到记录
        today = date.today()
        today_logs = AttendanceLog.query.filter(
            AttendanceLog.user_id == user.id,
            db.func.date(AttendanceLog.check_in_time) == today
        ).all()
        
        if today_logs:
            for log in today_logs:
                print(f"删除签到记录: ID={log.id}, 时间={log.check_in_time}")
                db.session.delete(log)
            db.session.commit()
            print(f"已删除 {len(today_logs)} 条今日签到记录")
        else:
            print("没有找到今日签到记录")
    else:
        print("未找到陈都用户")