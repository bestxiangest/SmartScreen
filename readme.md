# 智慧实验室电子班牌系统

一个基于Flask的智慧实验室管理系统，提供考勤管理、设备管理、环境监测、公告发布等功能的电子班牌解决方案。

## 📋 项目简介

智慧实验室电子班牌系统是一个现代化的实验室管理平台，旨在提高实验室的管理效率和用户体验。系统集成了多种功能模块，支持Web界面和API接口，可以满足不同场景下的使用需求。

## ✨ 主要功能

### 🔐 用户管理
- 用户注册、登录、注销
- JWT身份认证
- 用户资料管理
- 角色权限控制

### 📅 考勤管理
- 签到签退功能
- 考勤记录查询
- 考勤统计分析
- 二维码签到支持

### 🖥️ 设备管理
- 设备借用归还
- 设备状态监控
- 使用记录追踪
- 设备信息维护

### 🌡️ 环境监测
- 温度、湿度监测
- 光照强度检测
- CO2浓度监控
- 环境数据统计

### 📢 公告管理
- 公告发布编辑
- 公告分类管理
- 公告状态控制
- 历史公告查询

### 🗓️ 日程管理
- 实验室课程安排
- 日程查询功能
- 时间冲突检测

### 📁 文件管理
- 文件上传下载
- 多格式支持
- 文件大小限制
- 安全检查机制

### 🔬 实验室管理
- 实验室信息维护
- 实验室状态管理
- 容量控制

### 🛡️ 安全管理
- 安全检查记录
- 风险评估
- 安全统计分析

### 🤖 AI训练管理
- 训练任务管理
- 模型版本控制
- 训练进度监控

## 🛠️ 技术栈

### 后端技术
- **框架**: Flask 2.x
- **数据库**: MySQL
- **ORM**: SQLAlchemy
- **认证**: Flask-JWT-Extended
- **迁移**: Flask-Migrate
- **跨域**: Flask-CORS

### 前端技术
- **样式**: Tailwind CSS
- **图标**: Lucide Icons
- **模板**: Jinja2

### 开发工具
- **语言**: Python 3.8+
- **包管理**: pip
- **版本控制**: Git

## 📦 安装部署

### 环境要求
- Python 3.8 或更高版本
- MySQL 5.7 或更高版本
- pip 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/bestxiangest/SmartScreen.git
cd SmartScreen
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置数据库**
- 创建MySQL数据库
- 修改 `config.py` 中的数据库连接配置
- 执行数据库初始化脚本 `mysql.sql`

5. **配置环境变量**
```bash
# 创建 .env 文件（可选）
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=mysql://username:password@localhost/database_name
```

6. **运行应用**
```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 🚀 快速开始

### 基本使用

1. **访问系统**
   - 打开浏览器访问 `http://localhost:5000`
   - 使用默认管理员账号登录或注册新用户

2. **API调用**
   - 所有API接口都需要JWT认证（除了登录注册）
   - 在请求头中添加 `Authorization: Bearer <token>`

### API文档

详细的API文档请参考：
- [API_Documentation.md](./API_Documentation.md) - 完整API文档
- [API_Test_Documentation.md](./API_Test_Documentation.md) - API测试文档
- [QR_Code_API_Documentation.md](./QR_Code_API_Documentation.md) - 二维码API文档
- [Upload_Test_Documentation.md](./Upload_Test_Documentation.md) - 文件上传测试文档

### 示例API调用

```bash
# 用户登录
curl -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'

# 获取用户信息
curl -X GET "http://localhost:5000/api/v1/users/profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 签到
curl -X POST "http://localhost:5000/api/v1/attendance/checkin" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "lab_id": 1
  }'
```

## 📁 项目结构

```
SmartScreen/
├── app/                    # 应用主目录
│   ├── api/               # API路由模块
│   │   ├── auth.py        # 认证相关API
│   │   ├── users.py       # 用户管理API
│   │   ├── attendance.py  # 考勤管理API
│   │   ├── devices.py     # 设备管理API
│   │   ├── environmental.py # 环境监测API
│   │   ├── announcements.py # 公告管理API
│   │   ├── schedules.py   # 日程管理API
│   │   ├── upload.py      # 文件上传API
│   │   ├── labs.py        # 实验室管理API
│   │   ├── safety.py      # 安全管理API
│   │   ├── ai_training.py # AI训练管理API
│   │   └── user_profiles.py # 用户资料API
│   ├── helpers/           # 辅助函数
│   │   └── responses.py   # 响应格式化
│   ├── models.py          # 数据模型
│   ├── extensions.py      # Flask扩展
│   └── __init__.py        # 应用初始化
├── templates/             # HTML模板
├── static/               # 静态资源
├── uploads/              # 上传文件目录
├── migrations/           # 数据库迁移脚本
├── config.py             # 配置文件
├── app.py                # 应用入口
├── requirements.txt      # 依赖包列表
└── README.md            # 项目说明
```

## 🔧 配置说明

### 数据库配置

在 `config.py` 中修改数据库连接信息：

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/smartscreen'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = 'your-jwt-secret-key'
```

### 文件上传配置

```python
# 上传文件大小限制
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 允许的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
```

## 🧪 测试

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-flask

# 运行测试
pytest
```

### API测试

使用提供的测试文档进行API测试：

```bash
# 测试用户登录
curl -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'
```

## 📊 数据库设计

### 主要数据表

- **users**: 用户信息表
- **user_profiles**: 用户资料表
- **attendance_logs**: 考勤记录表
- **devices**: 设备信息表
- **device_usage_logs**: 设备使用记录表
- **environmental_logs**: 环境监测数据表
- **announcements**: 公告信息表
- **schedules**: 日程安排表
- **labs**: 实验室信息表
- **safety_checks**: 安全检查记录表
- **ai_training_tasks**: AI训练任务表

## 🔒 安全特性

- JWT身份认证
- 密码加密存储
- 文件类型验证
- 文件大小限制
- SQL注入防护
- XSS攻击防护
- CORS跨域控制

## 🌍 国际化

系统支持中文界面，所有时间数据使用北京时间（UTC+8）。

## 📝 更新日志

### v1.0.0
- 初始版本发布
- 完整的用户管理系统
- 考勤管理功能
- 设备管理功能
- 环境监测功能
- 公告管理功能
- 文件上传功能

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 项目Issues: [GitHub Issues](https://github.com/bestxiangest/SmartScreen/issues)
- 邮箱: zzningg@qq.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户。

---

**智慧实验室电子班牌系统** - 让实验室管理更智能、更高效！