#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧实验室电子班牌系统 - 数据库模型
"""

from app.extensions import db
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import json

# 北京时区
BEIJING_TZ = timezone(timedelta(hours=8))

def beijing_now():
    """获取北京时间"""
    return datetime.now(BEIJING_TZ)

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    full_name = db.Column(db.String(100), nullable=False, comment='真实姓名')
    major = db.Column(db.String(100), comment='专业')
    class_name = db.Column('class', db.String(50), comment='班级')
    email = db.Column(db.String(100), comment='邮箱地址')
    phone_number = db.Column(db.String(20), comment='手机号码')
    face_data = db.Column(db.LargeBinary, comment='用于人脸识别的生物特征数据')
    avatar_url = db.Column(db.String(255), comment='头像图片URL')
    created_at = db.Column(db.DateTime, default=beijing_now, comment='创建时间')
    
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
            'major': self.major,
            'class': self.class_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'face_data': self.face_data,
            'avatar_url': self.avatar_url,
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

class UserProfile(db.Model):
    """用户个人资料模型"""
    __tablename__ = 'user_profiles'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, comment='用户ID，关联users表的主键，同时也是本表主键')
    gender = db.Column(db.Enum('男', '女', '保密'), default='保密', comment='性别')
    birth_date = db.Column(db.Date, comment='出生日期')
    position = db.Column(db.String(100), comment='职务（例如：项目组长、成员、2023级负责人）')
    dormitory = db.Column(db.String(100), comment='宿舍信息（例如：2栋305室）')
    tech_stack = db.Column(db.JSON, comment='技术栈，使用JSON数组存储')
    
    # 关系
    user = db.relationship('User', backref=db.backref('profile', uselist=False, cascade='all, delete-orphan'))
    
    def to_dict(self):
        """转换为字典"""
        return {
            'user_id': self.user_id,
            'gender': self.gender,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'position': self.position,
            'dormitory': self.dormitory,
            'tech_stack': self.tech_stack
        }

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
    created_at = db.Column(db.DateTime, default=beijing_now, comment='发布时间')
    
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
    checkout_time = db.Column(db.DateTime, default=beijing_now, comment='借出时间')
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
    check_in_time = db.Column(db.DateTime, default=beijing_now, comment='签到时间')
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
    timestamp = db.Column(db.DateTime, default=beijing_now, comment='记录时间')
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

# 仓库物料管理模型
class MaterialCategory(db.Model):
    """物料分类模型"""
    __tablename__ = 'material_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='分类名称')
    description = db.Column(db.Text, comment='分类描述')
    parent_id = db.Column(db.Integer, db.ForeignKey('material_categories.id'), comment='父分类ID')
    sort_order = db.Column(db.Integer, default=0, comment='排序值')
    created_at = db.Column(db.DateTime, default=beijing_now, comment='创建时间')
    
    # 关系
    materials = db.relationship('Material', backref='category', lazy='dynamic')
    children = db.relationship('MaterialCategory', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Material(db.Model):
    """物料模型"""
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, comment='物料编码')
    name = db.Column(db.String(150), nullable=False, comment='物料名称')
    category_id = db.Column(db.Integer, db.ForeignKey('material_categories.id'), nullable=False)
    description = db.Column(db.Text, comment='物料描述')
    unit = db.Column(db.String(20), nullable=False, comment='计量单位')
    stock_quantity = db.Column(db.Integer, default=0, comment='当前库存数量')
    min_stock = db.Column(db.Integer, comment='最小安全库存')
    max_stock = db.Column(db.Integer, comment='最大库存')
    unit_price = db.Column(db.Numeric(10, 2), comment='单价')
    location = db.Column(db.String(100), comment='存放位置')
    supplier = db.Column(db.String(150), comment='供应商')
    created_at = db.Column(db.DateTime, default=beijing_now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=beijing_now, onupdate=beijing_now, comment='更新时间')
    
    # 关系
    transactions = db.relationship('MaterialTransaction', backref='material', lazy='dynamic')
    
    @property
    def status(self):
        """计算物料状态"""
        if self.stock_quantity == 0:
            return 'out_of_stock'
        elif self.min_stock and self.stock_quantity <= self.min_stock:
            return 'low_stock'
        else:
            return 'available'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'description': self.description,
            'unit': self.unit,
            'stock_quantity': self.stock_quantity,
            'min_stock': self.min_stock,
            'max_stock': self.max_stock,
            'unit_price': float(self.unit_price) if self.unit_price else None,
            'location': self.location,
            'supplier': self.supplier,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class MaterialRequest(db.Model):
    """物料申领模型"""
    __tablename__ = 'material_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(50), unique=True, nullable=False, comment='申领单号')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_name = db.Column(db.String(150), comment='关联的项目名称')
    status = db.Column(db.Enum('pending', 'approved', 'rejected', 'issued', 'returned', 'overdue'), 
                      default='pending', comment='申领状态')
    materials = db.Column(db.JSON, nullable=False, comment='申领的物料列表')
    approved_materials = db.Column(db.JSON, comment='批准的物料列表')
    expected_return_date = db.Column(db.Date, comment='预期归还日期')
    notes = db.Column(db.Text, comment='申领备注')
    approver_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='审批人ID')
    approved_at = db.Column(db.DateTime, comment='审批时间')
    approval_comment = db.Column(db.Text, comment='审批意见')
    created_at = db.Column(db.DateTime, default=beijing_now, comment='创建时间')
    
    # 关系
    user = db.relationship('User', foreign_keys=[user_id], backref='material_requests')
    approver = db.relationship('User', foreign_keys=[approver_id], backref='approved_requests')
    
    def to_dict(self):
        return {
            'id': self.id,
            'request_number': self.request_number,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'project_name': self.project_name,
            'status': self.status,
            'materials': self.materials,
            'approved_materials': self.approved_materials,
            'expected_return_date': self.expected_return_date.isoformat() if self.expected_return_date else None,
            'notes': self.notes,
            'approver_id': self.approver_id,
            'approver_name': self.approver.full_name if self.approver else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'approval_comment': self.approval_comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class MaterialTransaction(db.Model):
    """物料出入库记录模型"""
    __tablename__ = 'material_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    transaction_type = db.Column(db.Enum('in', 'out', 'return', 'adjust'), nullable=False, comment='交易类型')
    quantity = db.Column(db.Integer, nullable=False, comment='变动数量')
    before_quantity = db.Column(db.Integer, nullable=False, comment='变动前库存')
    after_quantity = db.Column(db.Integer, nullable=False, comment='变动后库存')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='操作人ID')
    request_id = db.Column(db.Integer, db.ForeignKey('material_requests.id'), comment='关联的申领单ID')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=beijing_now, comment='创建时间')
    
    # 关系
    user = db.relationship('User', backref='material_transactions')
    request = db.relationship('MaterialRequest', backref='transactions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'material_id': self.material_id,
            'material_name': self.material.name if self.material else None,
            'transaction_type': self.transaction_type,
            'quantity': self.quantity,
            'before_quantity': self.before_quantity,
            'after_quantity': self.after_quantity,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'request_id': self.request_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 维修工单管理模型
class MaintenanceOrder(db.Model):
    """维修工单模型"""
    __tablename__ = 'maintenance_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, comment='工单号')
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    fault_type = db.Column(db.Enum('hardware', 'software', 'network', 'power', 'other'), 
                          nullable=False, comment='故障类型')
    fault_description = db.Column(db.Text, nullable=False, comment='故障描述')
    images = db.Column(db.JSON, comment='故障图片URL列表')
    priority = db.Column(db.Enum('low', 'medium', 'high', 'urgent'), 
                        default='medium', comment='优先级')
    status = db.Column(db.Enum('pending', 'assigned', 'in_progress', 'completed', 'cancelled'), 
                      default='pending', comment='工单状态')
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='维修人员ID')
    reported_at = db.Column(db.DateTime, default=beijing_now, comment='报修时间')
    assigned_at = db.Column(db.DateTime, comment='分配时间')
    expected_completion = db.Column(db.DateTime, comment='预期完成时间')
    actual_completion = db.Column(db.DateTime, comment='实际完成时间')
    solution_description = db.Column(db.Text, comment='解决方案描述')
    maintenance_notes = db.Column(db.Text, comment='维修备注')
    completion_images = db.Column(db.JSON, comment='维修完成图片URL列表')
    parts_used = db.Column(db.JSON, comment='使用的零件列表')
    
    # 关系
    device = db.relationship('Device', backref='maintenance_orders')
    reporter = db.relationship('User', foreign_keys=[reporter_id], backref='reported_orders')
    assignee = db.relationship('User', foreign_keys=[assignee_id], backref='assigned_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'device_id': self.device_id,
            'device_name': self.device.device_name if self.device else None,
            'fault_type': self.fault_type,
            'fault_description': self.fault_description,
            'images': self.images,
            'priority': self.priority,
            'status': self.status,
            'reporter_id': self.reporter_id,
            'reporter_name': self.reporter.full_name if self.reporter else None,
            'assignee_id': self.assignee_id,
            'assignee_name': self.assignee.full_name if self.assignee else None,
            'reported_at': self.reported_at.isoformat() if self.reported_at else None,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'expected_completion': self.expected_completion.isoformat() if self.expected_completion else None,
            'actual_completion': self.actual_completion.isoformat() if self.actual_completion else None,
            'solution_description': self.solution_description,
            'maintenance_notes': self.maintenance_notes,
            'completion_images': self.completion_images,
            'parts_used': self.parts_used
        }

# 值班调度管理模型
class DutySchedule(db.Model):
    """值班安排与日志模型"""
    __tablename__ = 'duty_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    duty_date = db.Column(db.Date, nullable=False, comment='值班日期')
    shift_type = db.Column(db.Enum('morning', 'afternoon', 'evening', 'night'), 
                          nullable=False, comment='班次类型')
    start_time = db.Column(db.Time, nullable=False, comment='开始时间')
    end_time = db.Column(db.Time, nullable=False, comment='结束时间')
    location = db.Column(db.String(100), comment='值班地点')
    responsibilities = db.Column(db.JSON, comment='职责列表')
    status = db.Column(db.Enum('scheduled', 'completed', 'absent', 'leave', 'substituted'), 
                      default='scheduled', comment='值班状态')
    substitute_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='替班人ID')
    notes = db.Column(db.Text, comment='安排备注')
    check_in_time = db.Column(db.DateTime, comment='签到时间')
    check_in_location = db.Column(db.String(100), comment='签到地点')
    check_in_notes = db.Column(db.Text, comment='签到备注')
    check_out_time = db.Column(db.DateTime, comment='签退时间')
    summary = db.Column(db.Text, comment='工作总结')
    issues = db.Column(db.JSON, comment='遇到的问题列表')
    handover_notes = db.Column(db.Text, comment='交接班备注')
    created_at = db.Column(db.DateTime, default=beijing_now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=beijing_now, onupdate=beijing_now, comment='更新时间')
    
    # 关系
    user = db.relationship('User', foreign_keys=[user_id], backref='duty_schedules')
    substitute = db.relationship('User', foreign_keys=[substitute_id], backref='substitute_schedules')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'duty_date': self.duty_date.isoformat() if self.duty_date else None,
            'shift_type': self.shift_type,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'location': self.location,
            'responsibilities': self.responsibilities,
            'status': self.status,
            'substitute_id': self.substitute_id,
            'substitute_name': self.substitute.full_name if self.substitute else None,
            'notes': self.notes,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'check_in_location': self.check_in_location,
            'check_in_notes': self.check_in_notes,
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'summary': self.summary,
            'issues': self.issues,
            'handover_notes': self.handover_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }