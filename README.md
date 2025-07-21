# 智能电子班牌后端API

这是一个基于Flask的智能电子班牌后端系统，提供消息通知和实验室优秀项目管理功能。

## 功能特性

### 1. 消息通知管理
- 获取消息通知列表（支持分页、筛选）
- 创建新的消息通知
- 更新消息通知
- 删除消息通知

### 2. 实验室优秀项目管理
- 获取项目列表（支持分页、筛选）
- 创建新项目（包含项目成员）
- 更新项目信息
- 删除项目

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置数据库
1. 复制 `.env.example` 为 `.env`
2. 修改 `.env` 文件中的数据库配置
3. 导入 `mysql.sql` 文件到您的MySQL数据库

### 3. 运行应用
```bash
python app.py
```

应用将在 `http://localhost:5000` 启动

## API接口文档

### 消息通知接口

#### 获取消息通知列表
- **URL**: `GET /api/announcements`
- **参数**:
  - `page`: 页码（默认1）
  - `limit`: 每页数量（默认10）
  - `type`: 消息类型筛选
  - `is_important`: 是否重要（true/false）

#### 创建消息通知
- **URL**: `POST /api/announcements`
- **请求体**:
```json
{
  "title": "通知标题",
  "content": "通知内容",
  "author_name": "发布者",
  "type": "通知",
  "is_important": 0
}
```

#### 更新消息通知
- **URL**: `PUT /api/announcements/{id}`
- **请求体**: 同创建接口

#### 删除消息通知
- **URL**: `DELETE /api/announcements/{id}`

### 项目管理接口

#### 获取项目列表
- **URL**: `GET /api/projects`
- **参数**:
  - `page`: 页码（默认1）
  - `limit`: 每页数量（默认10）
  - `achievement_type`: 成果类型筛选

#### 创建项目
- **URL**: `POST /api/projects`
- **请求体**:
```json
{
  "project_name": "项目名称",
  "description": "项目描述",
  "achievement_type": "获奖",
  "achievement_details": "获奖详情",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "image_url": "/images/project.jpg",
  "members": [
    {
      "user_id": 1,
      "role_in_project": "负责人"
    }
  ]
}
```

#### 更新项目
- **URL**: `PUT /api/projects/{id}`
- **请求体**: 同创建接口

#### 删除项目
- **URL**: `DELETE /api/projects/{id}`

### 辅助接口

#### 获取用户列表
- **URL**: `GET /api/users`

## 响应格式

所有接口都使用统一的响应格式：

```json
{
  "success": true,
  "message": "操作成功",
  "data": {},
  "timestamp": "2025-01-20T10:30:00"
}
```

## 数据库表结构

### announcements（消息通知表）
- `id`: 主键
- `title`: 标题
- `content`: 内容
- `author_name`: 发布者
- `type`: 类型（通知、新闻、动态、安全提示、天气提示、名言金句）
- `is_important`: 是否重要
- `created_at`: 创建时间

### projects（项目表）
- `id`: 主键
- `project_name`: 项目名称
- `description`: 项目描述
- `achievement_type`: 成果类型（获奖、专利、软著）
- `achievement_details`: 成果详情
- `start_date`: 开始日期
- `end_date`: 结束日期
- `image_url`: 图片地址

### project_members（项目成员表）
- `project_id`: 项目ID
- `user_id`: 用户ID
- `role_in_project`: 项目角色

## 注意事项

1. 请确保MySQL数据库已正确配置并运行
2. 修改 `app.py` 中的数据库连接配置
3. 生产环境请关闭调试模式
4. 建议使用环境变量管理敏感配置信息