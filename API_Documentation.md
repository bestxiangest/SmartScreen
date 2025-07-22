# 智慧实验室电子班牌系统 API 文档

## 概述

本文档描述了智慧实验室电子班牌系统的所有API接口，包括请求格式、响应格式和使用示例。

### 基础信息

- **基础URL**: `http://127.0.0.1:5000/api/v1`
- **认证方式**: JWT Token (部分接口需要)
- **请求格式**: JSON
- **响应格式**: JSON

### 统一响应格式

#### 成功响应
```json
{
  "code": 200,
  "message": "操作成功",
  "success": true,
  "data": {}
}
```

#### 分页响应
```json
{
  "code": 200,
  "message": "获取成功",
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 100,
      "total_pages": 10,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

#### 错误响应
```json
{
  "code": 400,
  "message": "操作失败",
  "success": false,
  "details": "详细错误信息"
}
```

### 认证说明

需要认证的接口需要在请求头中包含JWT Token：
```
Authorization: Bearer <your_jwt_token>
```

---

## 1. 认证模块 (Auth)

### 1.1 用户登录

**接口地址**: `POST /auth/login`

**请求参数**:
```json
{
  "username": "用户名",
  "password": "密码"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "登录成功",
  "success": true,
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "full_name": "管理员",
      "email": "admin@example.com",
      "status": "active",
      "created_at": "2024-01-01T00:00:00"
    }
  }
}
```

### 1.2 获取用户信息

**接口地址**: `GET /auth/profile`

**认证**: 需要JWT Token

**响应示例**:
```json
{
  "code": 200,
  "message": "获取用户信息成功",
  "success": true,
  "data": {
    "id": 1,
    "username": "admin",
    "full_name": "管理员",
    "email": "admin@example.com",
    "status": "active",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

---

## 2. 通知公告模块 (Announcements)

### 2.1 获取通知公告列表

**接口地址**: `GET /announcements`

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `type` (string, 可选): 通知类型筛选
- `is_important` (boolean, 可选): 是否重要通知筛选

**响应示例**:
```json
{
  "code": 200,
  "message": "获取通知公告列表成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "title": "重要通知",
        "content": "通知内容",
        "author_name": "管理员",
        "type": "系统通知",
        "is_important": true,
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 2.2 创建通知公告

**接口地址**: `POST /announcements`

**请求参数**:
```json
{
  "title": "通知标题",
  "content": "通知内容",
  "author_name": "发布者姓名",
  "type": "通知类型",
  "is_important": false
}
```

### 2.3 更新通知公告

**接口地址**: `PUT /announcements/{id}`

**请求参数**: 同创建接口

### 2.4 删除通知公告

**接口地址**: `DELETE /announcements/{id}`

---

## 3. 项目成果模块 (Projects)

### 3.1 获取项目成果列表

**接口地址**: `GET /projects`

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `achievement_type` (string, 可选): 成果类型筛选

**响应示例**:
```json
{
  "code": 200,
  "message": "获取项目成果列表成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "project_name": "项目名称",
        "description": "项目描述",
        "achievement_type": "科研成果",
        "achievement_details": "成果详情",
        "image_url": "http://example.com/image.jpg",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 3.2 获取单个项目成果详情

**接口地址**: `GET /projects/{id}`

### 3.3 创建项目成果

**接口地址**: `POST /projects`

**请求参数**:
```json
{
  "project_name": "项目名称",
  "description": "项目描述",
  "achievement_type": "成果类型",
  "achievement_details": "成果详情",
  "image_url": "图片URL",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

### 3.4 更新项目成果

**接口地址**: `PUT /projects/{id}`

### 3.5 删除项目成果

**接口地址**: `DELETE /projects/{id}`

---

## 4. 课程表模块 (Schedules)

### 4.1 获取课程表列表

**接口地址**: `GET /schedules`

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `class_date` (string, 可选): 上课日期筛选，格式：YYYY-MM-DD

**响应示例**:
```json
{
  "code": 200,
  "message": "获取课程表列表成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "course_name": "课程名称",
        "teacher_name": "教师姓名",
        "classroom": "教室",
        "class_date": "2024-01-01",
        "start_time": "08:00:00",
        "end_time": "09:40:00",
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 4.2 创建课程安排

**接口地址**: `POST /schedules`

**请求参数**:
```json
{
  "course_name": "课程名称",
  "teacher_name": "教师姓名",
  "classroom": "教室",
  "class_date": "2024-01-01",
  "start_time": "08:00:00",
  "end_time": "09:40:00"
}
```

### 4.3 更新课程安排

**接口地址**: `PUT /schedules/{id}`

### 4.4 删除课程安排

**接口地址**: `DELETE /schedules/{id}`

---

## 5. 用户管理模块 (Users)

### 5.1 获取用户列表

**接口地址**: `GET /users`

**认证**: 需要JWT Token

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `role` (string, 可选): 角色筛选
- `status` (string, 可选): 状态筛选
- `search` (string, 可选): 搜索用户名或姓名

**响应示例**:
```json
{
  "code": 200,
  "message": "获取用户列表成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "username": "admin",
        "full_name": "管理员",
        "email": "admin@example.com",
        "status": "active",
        "created_at": "2024-01-01T00:00:00",
        "roles": [
          {
            "id": 1,
            "role_name": "管理员",
            "description": "系统管理员"
          }
        ]
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 5.2 获取角色列表

**接口地址**: `GET /roles`

**认证**: 需要JWT Token

**响应示例**:
```json
{
  "code": 200,
  "message": "获取角色列表成功",
  "success": true,
  "data": [
    {
      "id": 1,
      "role_name": "管理员",
      "description": "系统管理员"
    },
    {
      "id": 2,
      "role_name": "教师",
      "description": "教师用户"
    }
  ]
}
```

---

## 6. 设备管理模块 (Devices)

### 6.1 获取设备列表

**接口地址**: `GET /devices`

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `category_id` (int, 可选): 设备分类ID筛选
- `status` (string, 可选): 设备状态筛选

**响应示例**:
```json
{
  "code": 200,
  "message": "获取设备列表成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "device_name": "设备名称",
        "device_model": "设备型号",
        "category_id": 1,
        "status": "正常",
        "location": "设备位置",
        "purchase_date": "2024-01-01",
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 6.2 获取设备使用记录

**接口地址**: `GET /device-usage-logs`

**认证**: 需要JWT Token

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `device_id` (int, 可选): 设备ID筛选
- `user_id` (int, 可选): 用户ID筛选

---

## 7. 考勤管理模块 (Attendance)

### 7.1 获取考勤记录列表

**接口地址**: `GET /attendance`

**认证**: 需要JWT Token

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `user_id` (int, 可选): 用户ID筛选
- `date` (string, 可选): 日期筛选，格式：YYYY-MM-DD
- `method` (string, 可选): 考勤方式筛选，可选值：人脸识别、扫码、手动

**响应示例**:
```json
{
  "code": 200,
  "message": "获取考勤记录列表成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "user_id": 1,
        "full_name": "张三",
        "check_in_time": "2024-01-01T08:00:00",
        "check_out_time": "2024-01-01T17:00:00",
        "method": "人脸识别",
        "emotion_status": "开心"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 7.2 用户签到

**接口地址**: `POST /attendance/check-in`

**认证**: 需要JWT Token

**请求体**:
```json
{
  "method": "人脸识别",
  "emotion_status": "开心"
}
```

**参数说明**:
- `method` (string, 必填): 考勤方式，可选值：人脸识别、扫码、手动
- `emotion_status` (string, 可选): 情绪状态

**响应示例**:
```json
{
  "code": 201,
  "message": "签到成功",
  "success": true,
  "data": {
    "id": 1,
    "user_id": 1,
    "full_name": "张三",
    "check_in_time": "2024-01-01T08:00:00",
    "check_out_time": null,
    "method": "人脸识别",
    "emotion_status": "开心"
  }
}
```

### 7.3 生成每日二维码

**接口地址**: `GET /attendance/qr-code`

**认证**: 无需认证

**响应示例**:
```json
{
  "code": 200,
  "message": "生成二维码成功",
  "success": true,
  "data": {
    "qr_code_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "token": "a1b2c3d4e5f6g7h8",
    "date": "2024-01-01",
    "expires_at": "2024-01-01 23:59:59"
  }
}
```

**参数说明**:
- `qr_code_image`: Base64编码的二维码图片
- `token`: 当日有效的签到token
- `date`: 二维码生成日期
- `expires_at`: 二维码过期时间

### 7.4 二维码签到

**接口地址**: `POST /attendance/qr-checkin`

**认证**: 无需认证

**请求体**:
```json
{
  "token": "a1b2c3d4e5f6g7h8",
  "user_name": "张三",
  "emotion_status": "开心"
}
```

**参数说明**:
- `token` (string, 必填): 从二维码获取的当日token
- `user_name` (string, 必填): 用户真实姓名
- `emotion_status` (string, 可选): 情绪状态

**响应示例**:
```json
{
  "code": 201,
  "message": "张三 签到成功",
  "success": true,
  "data": {
    "user_name": "张三",
    "check_in_time": "2024-01-01T08:00:00",
    "method": "扫码"
  }
}
```

### 7.5 获取今日考勤状态

**接口地址**: `GET /attendance/today`

**认证**: 需要JWT Token

**响应示例**:
```json
{
  "code": 200,
  "message": "获取今日考勤状态成功",
  "success": true,
  "data": {
    "id": 1,
    "user_id": 1,
    "full_name": "张三",
    "check_in_time": "2024-01-01T08:00:00",
    "check_out_time": null,
    "method": "人脸识别",
    "emotion_status": "开心"
  }
}
```

---

## 8. 环境监测模块 (Environmental)

### 8.1 获取环境监测日志列表

**接口地址**: `GET /environmental-logs`

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `sensor_type` (string, 可选): 传感器类型筛选，可选值：温度、湿度、光照、CO2
- `lab_id` (int, 可选): 实验室ID筛选
- `start_time` (string, 可选): 开始时间，ISO格式
- `end_time` (string, 可选): 结束时间，ISO格式

**响应示例**:
```json
{
  "code": 200,
  "message": "获取环境监测日志列表成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "lab_id": 1,
        "sensor_type": "温度",
        "value": 25.5,
        "unit": "°C",
        "timestamp": "2024-01-01T08:00:00",
        "created_at": "2024-01-01T08:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 8.2 获取最新环境监测数据

**接口地址**: `GET /environmental-logs/latest`

**查询参数**:
- `lab_id` (int, 可选): 实验室ID筛选

**响应示例**:
```json
{
  "code": 200,
  "message": "获取最新环境监测数据成功",
  "success": true,
  "data": {
    "温度": {
      "id": 1,
      "lab_id": 1,
      "sensor_type": "温度",
      "value": 25.5,
      "unit": "°C",
      "timestamp": "2024-01-01T08:00:00"
    },
    "湿度": {
      "id": 2,
      "lab_id": 1,
      "sensor_type": "湿度",
      "value": 60.0,
      "unit": "%",
      "timestamp": "2024-01-01T08:00:00"
    }
  }
}
```

---

## 9. 实验室信息模块 (Labs)

### 9.1 获取实验室信息列表

**接口地址**: `GET /labs`

**响应示例**:
```json
{
  "code": 200,
  "message": "获取实验室信息列表成功",
  "success": true,
  "data": [
    {
      "id": 1,
      "lab_name": "实验室A",
      "location": "教学楼1层",
      "capacity": 30,
      "equipment_list": "设备清单",
      "responsible_person": "负责人",
      "contact_info": "联系方式",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

---

## 10. 安全须知模块 (Safety)

### 10.1 获取安全须知列表

**接口地址**: `GET /safety-guidelines`

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `category` (string, 可选): 安全类别筛选

### 10.2 获取单个安全须知详情

**接口地址**: `GET /safety-guidelines/{id}`

---

## 11. AI培养方案模块 (AI Training)

### 11.1 获取AI培养方案列表

**接口地址**: `GET /ai-training-plans`

**认证**: 需要JWT Token

**查询参数**:
- `page` (int, 可选): 页码，默认为1
- `limit` (int, 可选): 每页数量，默认为10
- `user_id` (int, 可选): 用户ID筛选
- `status` (string, 可选): 状态筛选，可选值：进行中、已完成

**响应示例**:
```json
{
  "code": 200,
  "message": "获取AI培养方案列表成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "user_id": 1,
        "plan_content": "培养方案内容",
        "status": "进行中",
        "generated_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 1,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权，需要登录 |
| 403 | 禁止访问，权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 使用示例

### JavaScript 示例

```javascript
// 登录
const login = async (username, password) => {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  });
  
  const result = await response.json();
  if (result.success) {
    localStorage.setItem('token', result.data.token);
    return result.data;
  } else {
    throw new Error(result.message);
  }
};

// 获取通知列表
const getAnnouncements = async (page = 1, limit = 10) => {
  const response = await fetch(`/api/v1/announcements?page=${page}&limit=${limit}`);
  const result = await response.json();
  
  if (result.success) {
    return result.data;
  } else {
    throw new Error(result.message);
  }
};

// 带认证的请求
const getProfile = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch('/api/v1/auth/profile', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const result = await response.json();
  if (result.success) {
    return result.data;
  } else {
    throw new Error(result.message);
  }
};
```

### Python 示例

```python
import requests
import json

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
    
    def login(self, username, password):
        url = f"{self.base_url}/auth/login"
        data = {"username": username, "password": password}
        
        response = requests.post(url, json=data)
        result = response.json()
        
        if result['success']:
            self.token = result['data']['token']
            return result['data']
        else:
            raise Exception(result['message'])
    
    def get_announcements(self, page=1, limit=10):
        url = f"{self.base_url}/announcements"
        params = {"page": page, "limit": limit}
        
        response = requests.get(url, params=params)
        result = response.json()
        
        if result['success']:
            return result['data']
        else:
            raise Exception(result['message'])
    
    def get_profile(self):
        url = f"{self.base_url}/auth/profile"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url, headers=headers)
        result = response.json()
        
        if result['success']:
            return result['data']
        else:
            raise Exception(result['message'])

# 使用示例
client = APIClient("http://127.0.0.1:5000/api/v1")
user_data = client.login("admin", "password")
announcements = client.get_announcements(page=1, limit=20)
profile = client.get_profile()
```

---

## 更新日志

- **v1.0.0** (2024-01-01): 初始版本，包含所有基础功能模块

---

## 联系方式

如有问题或建议，请联系开发团队。