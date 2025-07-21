# 智慧实验室电子班牌系统

一个基于Flask的智慧实验室电子班牌后端系统，提供完整的RESTful API接口。

## 🚀 功能特性

- 🔐 **用户认证与授权** - JWT身份认证，角色权限管理
- 📢 **公告管理** - 支持多种类型公告的发布与管理
- 🏆 **项目成果管理** - 获奖、专利、软著等成果记录
- 📅 **课程安排** - 课程表管理与查询
- 🔧 **设备管理** - 实验室设备借用与归还
- 📊 **考勤管理** - 多种考勤方式，统计分析
- 🏢 **实验室信息** - 实验室基本信息与文化展示
- 🛡️ **安全指南** - 安全规范与指导
- 🤖 **AI训练计划** - 个性化学习计划生成
- 🌡️ **环境监控** - 温湿度、光照等环境数据监控
- 📁 **文件上传** - 图片文件上传与管理

## 🛠️ 技术栈

- **后端框架**: Flask 2.3.3
- **数据库**: MySQL + SQLAlchemy ORM
- **身份认证**: Flask-JWT-Extended
- **跨域处理**: Flask-CORS
- **环境管理**: python-dotenv
- **密码加密**: bcrypt
- **文件处理**: Pillow

## 📁 项目结构

```
SmartScreen/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用工厂函数
│   ├── models.py          # 数据库模型
│   ├── main.py            # 主蓝图
│   ├── api/               # API蓝图
│   │   ├── __init__.py    # API蓝图初始化
│   │   ├── auth.py        # 认证相关API
│   │   ├── announcements.py  # 公告管理API
│   │   ├── projects.py    # 项目成果API
│   │   ├── schedules.py   # 课程安排API
│   │   ├── devices.py     # 设备管理API
│   │   ├── attendance.py  # 考勤管理API
│   │   ├── labs.py        # 实验室信息API
│   │   ├── safety.py      # 安全指南API
│   │   ├── ai_training.py # AI训练计划API
│   │   ├── environmental.py # 环境监控API
│   │   ├── upload.py      # 文件上传API
│   │   └── users.py       # 用户管理API
│   └── helpers/           # 辅助函数
│       ├── __init__.py
│       └── responses.py   # 统一响应格式
├── static/                # 静态文件
│   └── uploads/          # 上传文件目录
├── templates/             # 模板文件
├── uploads/              # 文件上传目录
├── app.py                # 简化版应用入口
├── config.py             # 配置文件
├── run.py                # 完整版应用启动文件
├── requirements.txt      # 依赖包列表
├── mysql.sql            # 数据库结构
├── .env.example         # 环境变量示例
└── README.md            # 项目说明
```

## 🚀 快速开始

### 1. 环境准备

确保已安装以下软件：
- Python 3.8+
- MySQL 5.7+ (可选，用于完整功能)
- pip

### 2. 克隆项目

```bash
git clone <repository-url>
cd SmartScreen
```

### 3. 安装依赖

```bash
# 安装基础依赖
pip install Flask Flask-CORS

# 或安装完整依赖
pip install -r requirements.txt
```

### 4. 快速启动（简化版）

```bash
# 直接运行简化版
python app.py
```

应用将在 `http://localhost:5000` 启动。

### 5. 完整功能启动

如需使用完整功能，请按以下步骤操作：

#### 5.1 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库连接等信息：

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=smartscreen
```

#### 5.2 初始化数据库

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE smartscreen CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 导入数据库结构
mysql -u root -p smartscreen < mysql.sql
```

#### 5.3 启动完整版应用

```bash
python run.py
```

## 📚 API 文档

### 基础接口

- `GET /` - 系统信息
- `GET /health` - 健康检查
- `GET /api/test` - API测试

### 认证接口 (完整版)

- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/profile` - 获取用户信息
- `POST /api/v1/auth/refresh` - 刷新令牌

### 公告管理 (完整版)

- `GET /api/v1/announcements` - 获取公告列表
- `POST /api/v1/announcements` - 创建公告
- `GET /api/v1/announcements/{id}` - 获取公告详情
- `PUT /api/v1/announcements/{id}` - 更新公告
- `DELETE /api/v1/announcements/{id}` - 删除公告

### 项目成果管理 (完整版)

- `GET /api/v1/projects` - 获取项目列表
- `POST /api/v1/projects` - 创建项目
- `GET /api/v1/projects/{id}` - 获取项目详情
- `PUT /api/v1/projects/{id}` - 更新项目
- `DELETE /api/v1/projects/{id}` - 删除项目

详细的API文档请参考 `API文档.md` 文件。

## 📋 统一响应格式

### 成功响应

```json
{
  "success": true,
  "message": "操作成功",
  "data": {},
  "code": 200,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 分页响应

```json
{
  "success": true,
  "message": "获取数据成功",
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "pages": 10
  },
  "code": 200,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 错误响应

```json
{
  "success": false,
  "message": "错误信息",
  "error_code": 400,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🚀 部署说明

### 开发环境

```bash
# 简化版
python app.py

# 完整版
export FLASK_CONFIG=development
python run.py
```

### 生产环境

```bash
export FLASK_CONFIG=production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker 部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## 🔧 开发指南

### 两种运行模式

1. **简化版 (app.py)**: 适合快速测试和演示，无需数据库
2. **完整版 (run.py)**: 包含所有功能，需要MySQL数据库

### 添加新的API接口

1. 在 `app/api/` 目录下创建或编辑相应的模块文件
2. 定义路由和处理函数
3. 在 `app/api/__init__.py` 中导入新模块
4. 使用统一的响应格式

### 数据库模型

所有数据库模型定义在 `app/models.py` 中，使用 SQLAlchemy ORM。

### 错误处理

使用 `app/helpers/responses.py` 中的辅助函数来生成统一的响应格式。

## 🧪 测试

```bash
# 安装测试依赖
pip install pytest pytest-flask

# 运行测试
pytest
```

## 📝 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 完整的API接口实现
- 用户认证与权限管理
- 数据库模型设计
- 统一响应格式

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- 项目链接: [https://github.com/yourusername/SmartScreen](https://github.com/yourusername/SmartScreen)

---

**智慧实验室电子班牌系统** - 让实验室管理更智能、更高效！