#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 数据库模型
"""

from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    full_name = db.Column(db.String(100), nullable=False, comment='真实姓名')
    email = db.Column(db.String(100), comment='邮箱地址')
    phone_number = db.Column(db.String(20), comment='手机号码')
    face_data = db.Column(db.LargeBinary, comment='用于人脸识别的生物特征数据')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    # 关系
    project_memberships = db.relationship('ProjectMember', backref='user', lazy='dynamic')
    attendance_logs = db.relationship('AttendanceLog', backref='user', lazy='dynamic')
    device_usage_logs = db.relationship('DeviceUsageLog', backref='user', lazy='dynamic')
    ai_training_plans = db.relationship('AITrainingPlan', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password, method='scrypt')
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'face_data': self.face_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Role(db.Model):
    """角色模型"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False, comment='角色名称')
    permissions = db.Column(db.JSON, comment='权限列表')
    
    def to_dict(self):
        return {
            'id': self.id,
            'role_name': self.role_name,
            'permissions': self.permissions
        }

class UserRole(db.Model):
    """用户角色关联模型"""
    __tablename__ = 'user_roles'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)

class Announcement(db.Model):
    """通知公告模型"""
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, comment='标题')
    content = db.Column(db.Text, nullable=False, comment='内容')
    author_name = db.Column(db.String(50), comment='发布者名称')
    type = db.Column(db.Enum('通知', '新闻', '动态', '安全提示', '天气提示', '名言金句'), 
                    nullable=False, comment='公告类型')
    is_important = db.Column(db.Boolean, default=False, comment='是否为重要通知')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='发布时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_name': self.author_name,
            'type': self.type,
            'is_important': self.is_important,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Project(db.Model):
    """项目成果模型"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False, comment='项目名称')
    description = db.Column(db.Text, comment='项目描述')
    achievement_type = db.Column(db.Enum('获奖', '专利', '软著'), nullable=False, comment='成果类型')
    achievement_details = db.Column(db.Text, comment='成果详情')
    start_date = db.Column(db.Date, comment='项目开始日期')
    end_date = db.Column(db.Date, comment='项目结束日期')
    image_url = db.Column(db.String(255), comment='项目展示图片地址')
    
    # 关系
    members = db.relationship('ProjectMember', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_members=True):
        result = {
            'id': self.id,
            'project_name': self.project_name,
            'description': self.description,
            'achievement_type': self.achievement_type,
            'achievement_details': self.achievement_details,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'image_url': self.image_url
        }
        
        if include_members:
            result['members'] = [member.to_dict() for member in self.members]
        
        return result

class ProjectMember(db.Model):
    """项目成员模型"""
    __tablename__ = 'project_members'
    
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_in_project = db.Column(db.String(50), comment='在项目中的角色')
    
    def to_dict(self):
        return {
            'id': self.user.id,
            'full_name': self.user.full_name,
            'role_in_project': self.role_in_project
        }

class DeviceCategory(db.Model):
    """设备分类模型"""
    __tablename__ = 'device_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False, comment='分类名称')
    
    # 关系
    devices = db.relationship('Device', backref='category', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name
        }

class Device(db.Model):
    """设备模型"""
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False, comment='设备名称')
    category_id = db.Column(db.Integer, db.ForeignKey('device_categories.id'), nullable=False)
    model = db.Column(db.String(100), comment='型号')
    status = db.Column(db.Enum('可用', '使用中', '维修中', '报废'), 
                      default='可用', nullable=False, comment='设备状态')
    location = db.Column(db.String(100), comment='存放位置')
    image_url = db.Column(db.String(255), comment='设备图片地址')
    purchase_date = db.Column(db.Date, comment='购置日期')
    
    # 关系
    usage_logs = db.relationship('DeviceUsageLog', backref='device', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_name': self.device_name,
            'category_id': self.category_id,
            'category_name': self.category.category_name if self.category else None,
            'model': self.model,
            'status': self.status,
            'location': self.location,
            'image_url': self.image_url,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None
        }

class DeviceUsageLog(db.Model):
    """设备使用记录模型"""
    __tablename__ = 'device_usage_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    checkout_time = db.Column(db.DateTime, default=datetime.utcnow, comment='借出时间')
    checkin_time = db.Column(db.DateTime, comment='归还时间')
    notes = db.Column(db.Text, comment='备注')
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_name': self.device.device_name if self.device else None,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'checkout_time': self.checkout_time.isoformat() if self.checkout_time else None,
            'checkin_time': self.checkin_time.isoformat() if self.checkin_time else None,
            'notes': self.notes
        }

class AttendanceLog(db.Model):
    """考勤记录模型"""
    __tablename__ = 'attendance_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    check_in_time = db.Column(db.DateTime, default=datetime.utcnow, comment='签到时间')
    check_out_time = db.Column(db.DateTime, comment='签出时间')
    method = db.Column(db.Enum('人脸识别', '扫码', '手动'), nullable=False, comment='考勤方式')
    emotion_status = db.Column(db.String(50), comment='AI情绪检测结果')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.user.full_name if self.user else None,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'method': self.method,
            'emotion_status': self.emotion_status
        }

class Schedule(db.Model):
    """课程表模型"""
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False, comment='课程名称')
    teacher_name = db.Column(db.String(50), comment='授课教师')
    class_date = db.Column(db.Date, nullable=False, comment='上课日期')
    start_time = db.Column(db.Time, nullable=False, comment='开始时间')
    end_time = db.Column(db.Time, nullable=False, comment='结束时间')
    location = db.Column(db.String(100), comment='上课地点')
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_name': self.course_name,
            'teacher_name': self.teacher_name,
            'class_date': self.class_date.isoformat() if self.class_date else None,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'location': self.location
        }

class Lab(db.Model):
    """实验室信息模型"""
    __tablename__ = 'labs'
    
    id = db.Column(db.Integer, primary_key=True)
    lab_name = db.Column(db.String(100), nullable=False, comment='实验室名称')
    description = db.Column(db.Text, comment='基地简介')
    culture_info = db.Column(db.JSON, comment='文化理念')
    logo_url = db.Column(db.String(255), comment='Logo图片地址')
    
    # 关系
    environmental_logs = db.relationship('EnvironmentalLog', backref='lab', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'lab_name': self.lab_name,
            'description': self.description,
            'culture_info': self.culture_info,
            'logo_url': self.logo_url
        }

class EnvironmentalLog(db.Model):
    """环境监测日志模型"""
    __tablename__ = 'environmental_logs'
    
    id = db.Column(db.BigInteger, primary_key=True)
    sensor_type = db.Column(db.Enum('温度', '湿度', '光照', 'CO2'), nullable=False, comment='传感器类型')
    value = db.Column(db.Numeric(10, 2), nullable=False, comment='监测数值')
    unit = db.Column(db.String(20), nullable=False, comment='单位')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, comment='记录时间')
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sensor_type': self.sensor_type,
            'value': float(self.value),
            'unit': self.unit,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'lab_id': self.lab_id
        }

class SafetyGuideline(db.Model):
    """安全须知模型"""
    __tablename__ = 'safety_guidelines'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False, comment='类别')
    title = db.Column(db.String(255), nullable=False, comment='标题')
    content = db.Column(db.Text, nullable=False, comment='详细内容')
    version = db.Column(db.String(20), comment='版本号')
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'title': self.title,
            'content': self.content,
            'version': self.version
        }

class AITrainingPlan(db.Model):
    """AI个性化培养方案模型"""
    __tablename__ = 'ai_training_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_content = db.Column(db.JSON, nullable=False, comment='培养方案详情')
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, comment='生成时间')
    status = db.Column(db.Enum('进行中', '已完成'), default='进行中', comment='方案状态')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'plan_content': self.plan_content,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'status': self.status
        }