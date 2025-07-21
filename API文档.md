智慧实验室电子班牌 - 后端API接口文档 (V1.1)
一、 简介与设计原则
本文档定义了智慧实验室电子班牌系统后端的所有API接口。API的设计遵循以下原则：

RESTful架构: 使用标准的HTTP方法 (GET, POST, PUT, DELETE) 对资源进行操作。

JSON数据格式: 所有请求体和响应体均使用 application/json 格式。

统一的URL结构: API根路径为 /api/v1，便于版本管理。

统一的响应结构: 所有接口都使用统一的响应格式，如下所示：

成功响应 (Success):

{
    "success": true,
    "message": "操作成功",
    "data": { ... }, // 或 [ ... ]
    "timestamp": "2025-07-21T10:30:00Z"
}

失败响应 (Error):

{
    "success": false,
    "message": "资源未找到",
    "error": "Not Found",
    "timestamp": "2025-07-21T10:30:00Z"
}

身份认证: 除登录接口外，所有需要权限的API请求都必须在HTTP头部包含 Authorization: Bearer <token> 字段。

二、 认证接口 (Authentication)
1. 用户登录
功能: 用户通过用户名和密码登录，获取JWT。

URL: /api/v1/auth/login

方法: POST

请求体:

{
    "username": "admin",
    "password": "password123"
}

成功响应 (200 OK):

{
    "success": true,
    "message": "登录成功",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user_info": {
            "id": 1,
            "full_name": "系统管理员",
            "role": "管理员"
        }
    },
    "timestamp": "..."
}

三、 消息通知接口 (Announcements)
1. 获取消息通知列表
功能: 分页获取通知列表，可按类型和重要性筛选。

URL: /api/v1/announcements

方法: GET

查询参数:

page (optional, integer, default: 1): 页码。

limit (optional, integer, default: 10): 每页数量。

type (optional, string): 按类型筛选。

is_important (optional, boolean): 按是否重要筛选。

成功响应 (200 OK):

{
    "success": true,
    "message": "获取成功",
    "data": {
        "items": [
            {
                "id": 1,
                "title": "实验室安全培训通知",
                "author_name": "黄老师",
                "type": "通知",
                "is_important": true,
                "created_at": "2025-07-18T11:00:00Z"
            }
        ],
        "total": 1
    },
    "timestamp": "..."
}

2. 创建新通知
功能: 发布一条新的通知。

URL: /api/v1/announcements

方法: POST

请求体:

{
    "title": "新设备到货通知",
    "content": "一批新的FPGA开发板已到货。",
    "author_name": "系统管理员",
    "type": "通知",
    "is_important": false
}

成功响应 (201 Created):

{
    "success": true,
    "message": "创建成功",
    "data": {
        "id": 2,
        "title": "新设备到货通知",
        "..." : "..."
    },
    "timestamp": "..."
}

3. 更新通知
功能: 修改指定ID的通知信息。

URL: /api/v1/announcements/<int:id>

方法: PUT

请求体: (同创建接口)

成功响应 (200 OK): (结构同上)

4. 删除通知
功能: 删除指定ID的通知。

URL: /api/v1/announcements/<int:id>

方法: DELETE

成功响应 (200 OK):

{
    "success": true,
    "message": "删除成功",
    "data": null,
    "timestamp": "..."
}

四、 项目管理接口 (Projects)
1. 获取项目列表
功能: 分页获取项目列表，可按成果类型筛选。

URL: /api/v1/projects

方法: GET

查询参数:

page (optional, integer, default: 1): 页码。

limit (optional, integer, default: 10): 每页数量。

achievement_type (optional, string): 按成果类型筛选。

成功响应 (200 OK): (结构同获取通知列表)

2. 创建新项目
功能: 添加一个新的项目成果。

URL: /api/v1/projects

方法: POST

请求体:

{
    "project_name": "AI情绪识别系统",
    "description": "基于深度学习的实时面部情绪识别。",
    "achievement_type": "软著",
    "achievement_details": "...",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "image_url": "/images/project.jpg",
    "members": [
        { "user_id": 3, "role_in_project": "负责人" },
        { "user_id": 4, "role_in_project": "组员" }
    ]
}

成功响应 (201 Created): (结构同创建通知)

3. 更新项目
功能: 修改指定ID的项目信息。

URL: /api/v1/projects/<int:id>

方法: PUT

请求体: (同创建接口)

成功响应 (200 OK): (结构同上)

4. 删除项目
功能: 删除指定ID的项目。

URL: /api/v1/projects/<int:id>

方法: DELETE

成功响应 (200 OK): (结构同删除通知)

五、 用户与设备接口 (Users & Devices)
1. 获取用户列表
功能: 获取所有用户列表，用于项目成员选择等。

URL: /api/v1/users

方法: GET

成功响应 (200 OK):

{
    "success": true,
    "message": "获取成功",
    "data": [
        {"id": 1, "full_name": "系统管理员"},
        {"id": 2, "full_name": "黄老师"},
        {"id": 3, "full_name": "吴文静"}
    ],
    "timestamp": "..."
}

2. 获取所有设备
功能: 分页获取设备列表，可按分类、状态筛选。

URL: /api/v1/devices

方法: GET

查询参数: page, limit, category_id, status

成功响应 (200 OK): (结构同获取通知列表)

3. 获取设备分类
功能: 获取所有设备分类列表。

URL: /api/v1/device-categories

方法: GET

成功响应 (200 OK): (结构同获取用户列表)

六、 考勤与环境接口 (IoT & Attendance)
1. 获取考勤记录
功能: 分页获取考勤日志。

URL: /api/v1/attendance-logs

方法: GET

查询参数: page, limit, user_id, start_date, end_date

成功响应 (200 OK): (结构同获取通知列表)

2. 考勤签到 (新增)
功能: 用户进行考勤签到，用于小程序等客户端。

URL: /api/v1/attendance-logs

方法: POST

请求体:

{
    "user_id": 3,
    "method": "小程序扫码"
}

成功响应 (201 Created):

{
    "success": true,
    "message": "签到成功",
    "data": {
        "log_id": 123,
        "user_id": 3,
        "full_name": "吴文静",
        "check_in_time": "2025-07-21T11:00:00Z",
        "method": "小程序扫码"
    },
    "timestamp": "..."
}

失败响应 (409 Conflict):

{
    "success": false,
    "message": "今日已签到，请勿重复操作",
    "error": "Already Checked In",
    "timestamp": "..."
}

3. 获取实时环境数据
功能: 获取实验室最新的环境监测数据。

URL: /api/v1/environment/now

方法: GET

成功响应 (200 OK):

{
    "success": true,
    "message": "获取成功",
    "data": {
        "temperature": {"value": 25.5, "unit": "°C"},
        "humidity": {"value": 60.2, "unit": "%"},
        "co2": {"value": 450, "unit": "ppm"}
    },
    "timestamp": "..."
}

七、 总览仪表盘接口 (Dashboard)
1. 获取总览核心数据
功能: 一次性获取总览页面所需的核心统计数据。

URL: /api/v1/dashboard/stats

方法: GET

成功响应 (200 OK):

{
    "success": true,
    "message": "获取成功",
    "data": {
        "device_count": 32,
        "ongoing_projects": 4,
        "today_attendance": 12,
        "pending_alerts": 1
    },
    "timestamp": "..."
}
