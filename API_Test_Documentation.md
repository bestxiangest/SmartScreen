# 智慧实验室电子班牌系统 - API 测试文档

本文档包含所有API接口的curl测试命令，适用于Postman等API测试工具。

## 基础信息

- **基础URL**: `http://localhost:5000`
- **认证方式**: JWT Token (Bearer Token)
- **Content-Type**: `application/json`

## 目录

1. [基础接口](#基础接口)
2. [认证模块](#认证模块)
3. [用户管理](#用户管理)
4. [角色管理](#角色管理)
5. [通知公告](#通知公告)
6. [考勤管理](#考勤管理)
7. [实验室信息](#实验室信息)
8. [设备管理](#设备管理)
9. [课程表管理](#课程表管理)
10. [安全须知](#安全须知)
11. [项目成果](#项目成果)
12. [用户个人资料](#用户个人资料)
13. [环境监测](#环境监测)
14. [文件上传](#文件上传)

---

## 基础接口

### 1. 健康检查

```bash
curl -X GET "http://localhost:5000/health"
```

### 2. 根路径

```bash
curl -X GET "http://localhost:5000/"
```

### 3. API测试

```bash
curl -X GET "http://localhost:5000/api/test"
```

---

## 认证模块

### 1. 用户登录

```bash
curl -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
```
```
{
	"code": 200,
	"data": {
		"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MzIzMDkzMywianRpIjoiNDU3ZjA2ZTctNGQ3Yy00NmJmLTk3YzUtZWE2MjdkMDYxODZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjciLCJuYmYiOjE3NTMyMzA5MzMsImNzcmYiOiJjMGYzY2ZlOC1kNmZkLTQ4MTEtYmYzNS03NDQ3ZDc3MDNjMzYiLCJleHAiOjE3NTMzMTczMzN9.UszoSf2a1lwxF0DXE_emE_974cujdNqjJWg1pYZdr0U",
		"user": {
			"created_at": "2025-07-21T14:59:57",
			"email": "1816054322@qq.com",
			"face_data": null,
			"full_name": "管理员",
			"id": 7,
			"major": "计算机科学与技术",
			"class": "2022级1班",
			"phone_number": "13964140811",
			"avatar_url": "http://xxx.com/images/admin.jpg",
			"username": "admin"
		}
	},
	"message": "登录成功",
	"success": true
}
```

### 2. 获取当前用户信息

```bash
curl -X GET "http://localhost:5000/api/v1/auth/profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"data": {
		"created_at": "2025-07-21T14:59:57",
		"email": "1816054322@qq.com",
		"face_data": null,
		"full_name": "管理员",
		"id": 7,
		"phone_number": "13964140811",
		"roles": [
			{
				"id": 3,
				"permissions": {
					"manage_all": true,
					"read": true,
					"write_all": true
				},
				"role_name": "管理员"
			}
		],
		"username": "admin"
	},
	"message": "获取用户信息成功",
	"success": true
}
```
### 3. 刷新JWT令牌

```bash
curl -X POST "http://localhost:5000/api/v1/auth/refresh" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"data": {
		"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MzIzMTAwOCwianRpIjoiZWY1OWFhNzQtMTIzOS00M2MzLWJhNjYtMWI4MmUwYjFkZmU0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjciLCJuYmYiOjE3NTMyMzEwMDgsImNzcmYiOiI4NjcyNTBiMy00Y2I2LTQzZDEtYjU3MS0xYTBkZWRiMTY2Y2QiLCJleHAiOjE3NTMzMTc0MDh9.m5ADM2NQzPy2VwHI2PJz9FzjY3KKe80QzZvgM58orUQ"
	},
	"message": "令牌刷新成功",
	"success": true
}
```
---

## 用户管理

### 1. 获取用户列表

```bash
curl -X GET "http://localhost:5000/api/v1/users?page=1&limit=10&role=管理员&search=张祖宁" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"data": {
		"items": [
			{
				"created_at": "2025-07-20T23:55:11",
				"email": "zhangzuning@example.com",
				"face_data": null,
				"full_name": "张祖宁",
				"major": "物联网工程",
				"class": "2023级1班",
				"avatar_url": "http://xxx.com/images/zhangzuning.jpg",
				"id": 6,
				"phone_number": "13800138104",
				"roles": [
					{
						"id": 1,
						"permissions": {
							"read": true,
							"write_self": true
						},
						"role_name": "学生"
					},
					{
						"id": 3,
						"permissions": {
							"manage_all": true,
							"read": true,
							"write_all": true
						},
						"role_name": "管理员"
					}
				],
				"username": "2024104"
			}
		],
		"pagination": {
			"has_next": false,
			"has_prev": false,
			"limit": 10,
			"page": 1,
			"total": 1,
			"total_pages": 1
		}
	},
	"message": "获取用户列表成功",
	"success": true
}
```

### 1.1 通过真名查询用户ID

```bash
# 通过真名查询用户ID
curl -X GET "http://localhost:5000/api/v1/users/search-by-name?full_name=张祖宁" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 查询管理员用户
curl -X GET "http://localhost:5000/api/v1/users/search-by-name?full_name=管理员" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "查询用户成功",
  "data": [
    {
      "id": 6,
      "full_name": "张祖宁",
      "username": "2024104"
    }
  ]
}
```

**错误响应示例**:
```json
{
  "code": 404,
  "success": false,
  "message": "未找到匹配的用户"
}
```

### 2. 创建用户

```bash
curl -X POST "http://localhost:5000/api/v1/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "username": "testuser",
    "password": "password123",
    "full_name": "测试用户",
    "major": "计算机科学与技术",
    "class": "2023级1班",
    "email": "test@example.com",
    "phone_number": "13800138000",
    "avatar_url": "http://xxx.com/images/testuser.jpg",
    "role_ids": [1, 2]
  }'
```
```
{
	"code": 201,
	"data": {
		"created_at": "2025-07-23T00:47:50",
		"email": "test@example.com",
		"face_data": null,
		"full_name": "测试用户",
		"major": "计算机科学与技术",
		"class": "2023级1班",
		"avatar_url": "http://xxx.com/images/testuser.jpg",
		"id": 12,
		"phone_number": "13800138000",
		"roles": [
			{
				"id": 2,
				"permissions": {
					"manage_courses": true,
					"read": true,
					"write_all": true
				},
				"role_name": "教师"
			}
		],
		"username": "testuser"
	},
	"message": "用户创建成功",
	"success": true
}
```

### 3. 获取单个用户详情

```bash
curl -X GET "http://localhost:5000/api/v1/users/6" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"data": {
		"created_at": "2025-07-20T23:55:11",
		"email": "zhangzuning@example.com",
		"face_data": null,
		"full_name": "张祖宁",
		"major": "物联网工程",
		"class": "2023级1班",
		"avatar_url": "http://xxx.com/images/zhangzuning.jpg",
		"id": 6,
		"phone_number": "13800138104",
		"roles": [
			{
				"id": 1,
				"permissions": {
					"read": true,
					"write_self": true
				},
				"role_name": "学生"
			},
			{
				"id": 3,
				"permissions": {
					"manage_all": true,
					"read": true,
					"write_all": true
				},
				"role_name": "管理员"
			}
		],
		"username": "2024104"
	},
	"message": "获取用户详情成功",
	"success": true
}
```

### 4. 更新用户信息

```bash
curl -X PUT "http://localhost:5000/api/v1/users/12" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "username": "updateduser",
    "full_name": "更新的用户",
    "major": "软件工程",
    "class": "2023级2班",
    "email": "updated@example.com",
    "phone_number": "13900139000",
    "avatar_url": "http://xxx.com/images/updateduser.jpg",
    "password": "newpassword123",
    "role_ids": [3]
  }'
```
```
{
	"code": 200,
	"data": {
		"created_at": "2025-07-23T00:47:50",
		"email": "updated@example.com",
		"face_data": null,
		"full_name": "更新的用户",
		"major": "软件工程",
		"class": "2023级2班",
		"avatar_url": "http://xxx.com/images/updateduser.jpg",
		"id": 12,
		"phone_number": "13900139000",
		"roles": [
			{
				"id": 3,
				"permissions": {
					"manage_all": true,
					"read": true,
					"write_all": true
				},
				"role_name": "管理员"
			}
		],
		"username": "updateduser"
	},
	"message": "用户信息更新成功",
	"success": true
}
```
---

## 角色管理

### 1. 获取角色列表

```bash
curl -X GET "http://localhost:5000/api/v1/roles" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"data": [
		{
			"id": 1,
			"role_name": "学生",
			"permissions": ["read", "write_self"]
		},
		{
			"id": 2,
			"role_name": "教师",
			"permissions": ["read", "write", "manage_students"]
		},
		{
			"id": 3,
			"role_name": "管理员",
			"permissions": ["all"]
		}
	],
	"message": "获取角色列表成功",
	"success": true
}
```

### 2. 创建角色

```bash
curl -X POST "http://localhost:5000/api/v1/roles" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "role_name": "实验室助理",
    "permissions": ["read", "write", "manage_devices"]
  }'
```

**响应示例:**
```json
{
	"code": 201,
	"data": {
		"id": 4,
		"role_name": "实验室助理",
		"permissions": ["read", "write", "manage_devices"]
	},
	"message": "角色创建成功",
	"success": true
}
```

### 3. 获取角色详情

```bash
curl -X GET "http://localhost:5000/api/v1/roles/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"id": 1,
		"role_name": "学生",
		"permissions": ["read", "write_self"]
	},
	"message": "获取角色详情成功",
	"success": true
}
```

### 4. 更新角色

```bash
curl -X PUT "http://localhost:5000/api/v1/roles/4" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "role_name": "高级实验室助理",
    "permissions": ["read", "write", "manage_devices", "manage_attendance"]
  }'
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"id": 4,
		"role_name": "高级实验室助理",
		"permissions": ["read", "write", "manage_devices", "manage_attendance"]
	},
	"message": "角色信息更新成功",
	"success": true
}
```

### 5. 删除角色

```bash
curl -X DELETE "http://localhost:5000/api/v1/roles/4" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"message": "角色删除成功",
	"success": true
}
```

**注意事项:**
- 删除角色前需要确保没有用户使用该角色
- 如果有用户使用该角色，删除操作会失败并返回错误信息

### 6. 获取用户角色

```bash
curl -X GET "http://localhost:5000/api/v1/users/1/roles" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"data": [
		{
			"id": 1,
			"role_name": "学生",
			"permissions": ["read", "write_self"]
		},
		{
			"id": 3,
			"role_name": "管理员",
			"permissions": ["all"]
		}
	],
	"message": "获取用户角色成功",
	"success": true
}
```

### 7. 更新用户角色

```bash
curl -X PUT "http://localhost:5000/api/v1/users/1/roles" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "role_ids": [1, 2]
  }'
```

**响应示例:**
```json
{
	"code": 200,
	"data": [
		{
			"id": 1,
			"role_name": "学生",
			"permissions": ["read", "write_self"]
		},
		{
			"id": 2,
			"role_name": "教师",
			"permissions": ["read", "write", "manage_students"]
		}
	],
	"message": "用户角色更新成功",
	"success": true
}
```

**字段说明:**
- `role_name`: 角色名称（必填，唯一）
- `permissions`: 权限列表（可选，JSON数组格式）
- `role_ids`: 角色ID列表（用于用户角色分配）

**常用权限说明:**
- `read`: 读取权限
- `write`: 写入权限
- `write_self`: 仅能修改自己的信息
- `write_all`: 可以修改所有信息
- `manage_all`: 管理所有功能
- `manage_students`: 管理学生
- `manage_devices`: 管理设备
- `manage_attendance`: 管理考勤
- `all`: 所有权限

---

## 通知公告

### 1. 获取通知公告列表

```bash
curl -X GET "http://localhost:5000/api/v1/announcements?page=1&limit=10&type=通知&is_important=true" \
  -H "Content-Type: application/json"
```
```
{
	"code": 200,
	"data": {
		"items": [],
		"pagination": {
			"has_next": false,
			"has_prev": false,
			"limit": 10,
			"page": 1,
			"total": 0,
			"total_pages": 0
		}
	},
	"message": "获取通知公告列表成功",
	"success": true
}
```

### 2. 创建通知公告

```bash
curl -X POST "http://localhost:5000/api/v1/announcements" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "重要通知",
    "content": "这是一条重要的通知内容",
    "author_name": "管理员",
    "type": "通知",
    "is_important": true
  }'
```
```
{
	"code": 201,
	"data": {
		"author_name": "管理员",
		"content": "这是一条重要的通知内容",
		"created_at": "2025-07-23T01:11:21",
		"id": 8,
		"is_important": true,
		"title": "重要通知",
		"type": "通知"
	},
	"message": "创建通知公告成功",
	"success": true
}
```
### 3. 获取单个通知公告详情

```bash
curl -X GET "http://localhost:5000/api/v1/announcements/1" \
  -H "Content-Type: application/json"
```
```
{
	"code": 200,
	"data": {
		"author_name": "黄老师",
		"content": "本周五下午2点将进行全体成员安全培训，请务必参加。",
		"created_at": "2025-07-18T11:00:00",
		"id": 1,
		"is_important": true,
		"title": "实验室安全培训通知",
		"type": "通知"
	},
	"message": "获取通知公告详情成功",
	"success": true
}
```
### 4. 更新通知公告

```bash
curl -X PUT "http://localhost:5000/api/v1/announcements/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "更新的通知",
    "content": "更新后的通知内容",
    "author_name": "系统管理员",
    "type": "新闻",
    "is_important": false
  }'
```
```
{
	"code": 200,
	"data": {
		"author_name": "系统管理员",
		"content": "更新后的通知内容",
		"created_at": "2025-07-18T11:00:00",
		"id": 1,
		"is_important": false,
		"title": "更新的通知",
		"type": "新闻"
	},
	"message": "更新通知公告成功",
	"success": true
}
```
### 5. 删除通知公告

```bash
curl -X DELETE "http://localhost:5000/api/v1/announcements/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"message": "删除通知公告成功",
	"success": true
}
```
---

## 考勤管理

### 1. 获取考勤记录列表

```bash
curl -X GET "http://localhost:5000/api/v1/attendance?page=1&limit=10&full_name=张&date=2024-01-15&method=人脸识别" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"data": {
		"items": [
			{
				"check_in_time": "2025-07-22T06:45:31",
				"check_out_time": null,
				"emotion_status": "专注",
				"full_name": "张高炜",
				"id": 8,
				"method": "扫码",
				"user_id": 11
			},
			{
				"check_in_time": "2025-07-22T03:45:38",
				"check_out_time": null,
				"emotion_status": "开心",
				"full_name": "陈都",
				"id": 7,
				"method": "扫码",
				"user_id": 8
			},
			{
				"check_in_time": "2025-07-22T02:51:03",
				"check_out_time": null,
				"emotion_status": "开心",
				"full_name": "张祖宁",
				"id": 4,
				"method": "扫码",
				"user_id": 6
			}
		],
		"pagination": {
			"has_next": false,
			"has_prev": false,
			"limit": 10,
			"page": 1,
			"total": 3,
			"total_pages": 1
		}
	},
	"message": "获取考勤记录列表成功",
	"success": true
}
```

### 2. 签到

```bash
curl -X POST "http://localhost:5000/api/v1/attendance/check-in" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "method": "人脸识别",
    "emotion_status": "开心"
  }'
```
```
{
	"code": 201,
	"data": {
		"check_in_time": "2025-07-23T01:17:15",
		"check_out_time": null,
		"emotion_status": "开心",
		"full_name": "管理员",
		"id": 9,
		"method": "人脸识别",
		"user_id": 7
	},
	"message": "签到成功",
	"success": true
}
```

### 3. 签出

```bash
curl -X PUT "http://localhost:5000/api/v1/attendance/1/check-out" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"data": {
		"check_in_time": "2025-07-23T01:17:15",
		"check_out_time": "2025-07-23T01:18:37",
		"emotion_status": "开心",
		"full_name": "管理员",
		"id": 9,
		"method": "人脸识别",
		"user_id": 7
	},
	"message": "签出成功",
	"success": true
}
```
### 4. 获取今日考勤状态

```bash
curl -X GET "http://localhost:5000/api/v1/attendance/today" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"data": {
		"check_in_time": "2025-07-23T01:17:15",
		"check_out_time": "2025-07-23T01:18:37",
		"emotion_status": "开心",
		"full_name": "管理员",
		"id": 9,
		"method": "人脸识别",
		"user_id": 7
	},
	"message": "获取今日考勤状态成功",
	"success": true
}
```
### 5. 获取考勤统计

```bash
curl -X GET "http://localhost:5000/api/v1/attendance/statistics?user_id=1&full_name=张三&start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"data": {
		"completed_days": 1,
		"incomplete_days": 0,
		"method_statistics": {
			"人脸识别": 1
		},
		"total_attendance_days": 1
	},
	"message": "获取考勤统计成功",
	"success": true
}
```

### 6. 管理员控制签到

```bash
curl -X POST "http://localhost:5000/api/v1/attendance/admin/check-in" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "full_name": "张三",
    "method": "手动",
    "emotion_status": "正常"
  }'
```
```
{
	"code": 201,
	"data": {
		"check_in_time": "2024-01-16T08:30:00Z",
		"check_out_time": null,
		"emotion_status": "正常",
		"full_name": "张三",
		"id": 3,
		"method": "手动",
		"user_id": 1
	},
	"message": "管理员为 张三 签到成功",
	"success": true
}
```

### 7. 管理员控制签退

```bash
curl -X POST "http://localhost:5000/api/v1/attendance/admin/check-out" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "full_name": "张三"
  }'
```
```
{
	"code": 200,
	"data": {
		"check_in_time": "2024-01-16T08:30:00Z",
		"check_out_time": "2024-01-16T17:30:00Z",
		"emotion_status": "正常",
		"full_name": "张三",
		"id": 3,
		"method": "手动",
		"user_id": 1
	},
	"message": "管理员为 张三 签退成功",
	"success": true
}
```
---

## 实验室信息

### 1. 获取实验室信息列表

```bash
curl -X GET "http://localhost:5000/api/v1/labs" \
  -H "Content-Type: application/json"
```
```
{
	"code": 200,
	"data": [
		{
			"culture_info": {
				"main_culture": "不忘初心，砥砺前行",
				"values": "四个YU之道"
			},
			"description": "一个集物联网感知、智能交互与信息化管理于一体的实验室智能终端系统。",
			"id": 1,
			"lab_name": "通信电子创新基地",
			"logo_url": "/images/lab_logo.png"
		}
	],
	"message": "获取实验室信息列表成功",
	"success": true
}
```
### 2. 创建实验室信息

```bash
curl -X POST "http://localhost:5000/api/v1/labs" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "lab_name": "智能计算实验室",
    "description": "专注于人工智能和机器学习研究的实验室",
    "culture_info": {
      "vision": "成为世界一流的AI研究中心",
      "mission": "推动人工智能技术发展",
      "values": ["创新", "协作", "卓越"]
    },
    "logo_url": "https://example.com/logo.png"
  }'
```
```
{
	"code": 201,
	"data": {
		"culture_info": {
			"mission": "推动人工智能技术发展",
			"values": [
				"创新",
				"协作",
				"卓越"
			],
			"vision": "成为世界一流的AI研究中心"
		},
		"description": "专注于人工智能和机器学习研究的实验室",
		"id": 2,
		"lab_name": "智能计算实验室",
		"logo_url": "https://example.com/logo.png"
	},
	"message": "创建实验室信息成功",
	"success": true
}
```

### 3. 获取单个实验室详情

```bash
curl -X GET "http://localhost:5000/api/v1/labs/1" \
  -H "Content-Type: application/json"
```
```
{
	"code": 200,
	"data": {
		"culture_info": {
			"main_culture": "不忘初心，砥砺前行",
			"values": "四个YU之道"
		},
		"description": "一个集物联网感知、智能交互与信息化管理于一体的实验室智能终端系统。",
		"id": 1,
		"lab_name": "通信电子创新基地",
		"logo_url": "/images/lab_logo.png"
	},
	"message": "获取实验室详情成功",
	"success": true
}
```
### 4. 更新实验室信息

```bash
curl -X PUT "http://localhost:5000/api/v1/labs/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "lab_name": "更新的实验室名称",
    "description": "更新的实验室描述",
    "culture_info": {
      "vision": "更新的愿景",
      "mission": "更新的使命",
      "values": ["创新", "合作"]
    },
    "logo_url": "https://example.com/new-logo.png"
  }'
```
```
{
	"code": 200,
	"data": {
		"culture_info": {
			"mission": "更新的使命",
			"values": [
				"创新",
				"合作"
			],
			"vision": "更新的愿景"
		},
		"description": "更新的实验室描述",
		"id": 1,
		"lab_name": "更新的实验室名称",
		"logo_url": "https://example.com/new-logo.png"
	},
	"message": "更新实验室信息成功",
	"success": true
}
```
### 5. 删除实验室信息

```bash
curl -X DELETE "http://localhost:5000/api/v1/labs/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"message": "删除实验室信息成功",
	"success": true
}
```
### 6. 获取默认实验室信息

```bash
curl -X GET "http://localhost:5000/api/v1/labs/default" \
  -H "Content-Type: application/json"
```
```
{
	"code": 200,
	"data": {
		"culture_info": {
			"mission": "更新的使命",
			"values": [
				"创新",
				"合作"
			],
			"vision": "更新的愿景"
		},
		"description": "更新的实验室描述",
		"id": 1,
		"lab_name": "更新的实验室名称",
		"logo_url": "https://example.com/new-logo.png"
	},
	"message": "获取默认实验室信息成功",
	"success": true
}
```
---

## 设备管理

### 设备分类

#### 1. 获取设备分类列表

```bash
curl -X GET "http://localhost:5000/api/v1/device-categories" \
  -H "Content-Type: application/json"
```
```
{
	"code": 200,
	"data": [
		{
			"category_name": "动手实践",
			"id": 3
		},
		{
			"category_name": "开发平台",
			"id": 2
		},
		{
			"category_name": "测量仪器",
			"id": 1
		}
	],
	"message": "获取设备分类列表成功",
	"success": true
}
```

#### 2. 创建设备分类

```bash
curl -X POST "http://localhost:5000/api/v1/device-categories" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "category_name": "计算设备"
  }'
```
```
{
	"code": 201,
	"data": {
		"category_name": "计算设备",
		"id": 4
	},
	"message": "创建设备分类成功",
	"success": true
}
```
#### 3. 更新设备分类

```bash
curl -X PUT "http://localhost:5000/api/v1/device-categories/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "category_name": "更新的分类名称"
  }'
```
```
{
	"code": 200,
	"data": {
		"category_name": "更新的分类名称",
		"id": 4
	},
	"message": "更新设备分类成功",
	"success": true
}
```

#### 4. 删除设备分类

```bash
curl -X DELETE "http://localhost:5000/api/v1/device-categories/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"message": "删除设备分类成功",
	"success": true
}
```

### 设备管理

#### 1. 获取设备列表

```bash
curl -X GET "http://localhost:5000/api/v1/devices?page=1&limit=10&category_id=1&status=可用" \
  -H "Content-Type: application/json"
```
```
{
	"code": 200,
	"data": {
		"items": [
			{
				"category_id": 2,
				"category_name": "开发平台",
				"device_name": "FPGA开发套件",
				"id": 6,
				"image_url": "/images/devices/zynq7000.png",
				"location": "C区-实验台2",
				"model": "Xilinx Zynq-7000",
				"purchase_date": null,
				"status": "可用"
			},
			{
				"category_id": 2,
				"category_name": "开发平台",
				"device_name": "Linux开发套件",
				"id": 5,
				"image_url": "/images/devices/linux_kit.png",
				"location": "C区-实验台1",
				"model": "自研平台 v2.0",
				"purchase_date": null,
				"status": "使用中"
			}
		],
		"pagination": {
			"has_next": false,
			"has_prev": false,
			"limit": 10,
			"page": 1,
			"total": 2,
			"total_pages": 1
		}
	},
	"message": "获取设备列表成功",
	"success": true
}
```

#### 2. 创建设备

```bash
curl -X POST "http://localhost:5000/api/v1/devices" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "device_name": "高性能服务器",
    "category_id": 1,
    "model": "Dell PowerEdge R750",
    "status": "可用",
    "location": "机房A-01",
    "image_url": "https://example.com/device.jpg",
    "purchase_date": "2024-01-15"
  }'
```
```
{
	"code": 201,
	"data": {
		"category_id": 1,
		"category_name": "测量仪器",
		"device_name": "高性能服务器",
		"id": 9,
		"image_url": "https://example.com/device.jpg",
		"location": "机房A-01",
		"model": "Dell PowerEdge R750",
		"purchase_date": "2024-01-15",
		"status": "可用"
	},
	"message": "创建设备成功",
	"success": true
}
```
---

## 课程表管理

### 1. 获取课程表列表

```bash
curl -X GET "http://localhost:5000/api/v1/schedules?page=1&limit=10&class_date=2024-01-15" \
  -H "Content-Type: application/json"
```

### 2. 创建课程安排

```bash
curl -X POST "http://localhost:5000/api/v1/schedules" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "course_name": "人工智能基础",
    "teacher_name": "张教授",
    "class_date": "2024-01-15",
    "start_time": "09:00",
    "end_time": "11:00",
    "location": "实验室A-101"
  }'
```

### 3. 获取单个课程安排详情

```bash
curl -X GET "http://localhost:5000/api/v1/schedules/1" \
  -H "Content-Type: application/json"
```

### 4. 更新课程安排

```bash
curl -X PUT "http://localhost:5000/api/v1/schedules/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "course_name": "机器学习进阶",
    "teacher_name": "李教授",
    "class_date": "2024-01-16",
    "start_time": "14:00",
    "end_time": "16:00",
    "location": "实验室B-201"
  }'
```

---

## 安全须知

### 1. 获取安全须知列表

```bash
curl -X GET "http://localhost:5000/api/v1/safety-guidelines?page=1&limit=10&category=实验室安全" \
  -H "Content-Type: application/json"
```

### 2. 创建安全须知

```bash
curl -X POST "http://localhost:5000/api/v1/safety-guidelines" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "category": "实验室安全",
    "title": "设备操作安全规范",
    "content": "1. 操作前请仔细阅读设备说明书\n2. 确保设备接地良好\n3. 禁止带电操作",
    "version": "v1.0"
  }'
```

### 3. 获取单个安全须知详情

```bash
curl -X GET "http://localhost:5000/api/v1/safety-guidelines/1" \
  -H "Content-Type: application/json"
```

### 4. 更新安全须知

```bash
curl -X PUT "http://localhost:5000/api/v1/safety-guidelines/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "category": "设备安全",
    "title": "更新的安全规范",
    "content": "更新的安全须知内容",
    "version": "v1.1"
  }'
```

### 5. 删除安全须知

```bash
curl -X DELETE "http://localhost:5000/api/v1/safety-guidelines/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6. 获取安全须知类别列表

```bash
curl -X GET "http://localhost:5000/api/v1/safety-guidelines/categories" \
  -H "Content-Type: application/json"
```

---

## 项目成果

### 1. 获取项目成果列表

```bash
curl -X GET "http://localhost:5000/api/v1/projects?page=1&limit=10&achievement_type=获奖" \
  -H "Content-Type: application/json"
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"items": [
			{
				"achievement_details": "2024年（第17届）中国大学生计算机设计大赛江西省级赛 一等奖",
				"achievement_type": "获奖",
				"description": "该系统利用多种传感器实时监测大棚环境，并通过云平台进行数据分析和远程控制，实现蔬菜种植的智能化管理。",
				"end_date": "2024-06-01",
				"id": 1,
				"image_url": "/static/uploads/2a60b077-4208-4e24-bf34-91a03f475eb9.jpg",
				"members": [],
				"project_name": "基于物联网技术的智慧蔬菜大棚监测系统",
				"start_date": "2023-09-01"
			}
		],
		"pagination": {
			"has_next": false,
			"has_prev": false,
			"limit": 10,
			"page": 1,
			"total": 1,
			"total_pages": 1
		}
	},
	"message": "获取项目成果列表成功",
	"success": true
}
```

### 2. 创建项目成果

```bash
curl -X POST "http://localhost:5000/api/v1/projects" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "project_name": "智能图像识别系统",
    "description": "基于深度学习的图像识别系统，可以识别多种物体",
    "achievement_type": "获奖",
    "achievement_details": "2024年全国大学生创新创业大赛二等奖",
    "start_date": "2024-01-01",
    "end_date": "2024-06-30",
    "image_url": "https://example.com/project.jpg",
    "members": [
      {
        "user_id": 6,
        "role_in_project": "项目负责人"
      },
      {
        "user_id": 8,
        "role_in_project": "技术开发"
      }
    ]
  }'
```
```
{
	"code": 201,
	"data": {
		"achievement_details": "2024年全国大学生创新创业大赛二等奖",
		"achievement_type": "获奖",
		"description": "基于深度学习的图像识别系统，可以识别多种物体",
		"end_date": "2024-06-30",
		"id": 3,
		"image_url": "https://example.com/project.jpg",
		"members": [
			{
				"full_name": "张祖宁",
				"id": 6,
				"role_in_project": "项目负责人"
			},
			{
				"full_name": "陈都",
				"id": 8,
				"role_in_project": "技术开发"
			}
		],
		"project_name": "智能图像识别系统",
		"start_date": "2024-01-01"
	},
	"message": "创建项目成果成功",
	"success": true
}
```

### 3. 获取单个项目成果详情

```bash
curl -X GET "http://localhost:5000/api/v1/projects/1" \
  -H "Content-Type: application/json"
```
```
{
	"code": 200,
	"data": {
		"achievement_details": "2024年（第17届）中国大学生计算机设计大赛江西省级赛 一等奖",
		"achievement_type": "获奖",
		"description": "该系统利用多种传感器实时监测大棚环境，并通过云平台进行数据分析和远程控制，实现蔬菜种植的智能化管理。",
		"end_date": "2024-06-01",
		"id": 1,
		"image_url": "/static/uploads/2a60b077-4208-4e24-bf34-91a03f475eb9.jpg",
		"members": [],
		"project_name": "基于物联网技术的智慧蔬菜大棚监测系统",
		"start_date": "2023-09-01"
	},
	"message": "获取项目成果详情成功",
	"success": true
}
```

### 4. 更新项目成果

```bash
curl -X PUT "http://localhost:5000/api/v1/projects/3" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "project_name": "更新的项目名称",
    "description": "更新的项目描述",
    "achievement_type": "专利",
    "achievement_details": "已获得国家发明专利授权",
    "start_date": "2024-01-01",
    "end_date": "2024-05-31",
    "image_url": "https://example.com/updated-project.jpg",
    "members": [
      {
        "user_id": 6,
        "role_in_project": "项目负责人"
      },
      {
        "user_id": 8,
        "role_in_project": "研发工程师"
      }
    ]
  }'
```
```
{
	"code": 200,
	"data": {
		"achievement_details": "已获得国家发明专利授权",
		"achievement_type": "专利",
		"description": "更新的项目描述",
		"end_date": "2024-05-31",
		"id": 3,
		"image_url": "https://example.com/updated-project.jpg",
		"members": [
			{
				"full_name": "张祖宁",
				"id": 6,
				"role_in_project": "项目负责人"
			},
			{
				"full_name": "陈都",
				"id": 8,
				"role_in_project": "研发工程师"
			}
		],
		"project_name": "更新的项目名称",
		"start_date": "2024-01-01"
	},
	"message": "更新项目成果成功",
	"success": true
}
```

### 5. 删除项目成果

```bash
curl -X DELETE "http://localhost:5000/api/v1/projects/3" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
```
{
	"code": 200,
	"message": "删除项目成果成功",
	"success": true
}
```

**字段说明:**
- `project_name`: 项目名称（必填）
- `description`: 项目描述（可选）
- `achievement_type`: 成果类型（必填，可选值：'获奖', '专利', '软著'）
- `achievement_details`: 成果详情（可选）
- `start_date`: 项目开始日期（可选，格式：YYYY-MM-DD）
- `end_date`: 项目结束日期（可选，格式：YYYY-MM-DD）
- `image_url`: 项目展示图片地址（可选）
- `members`: 项目成员列表（可选），包含：
  - `user_id`: 用户ID（必填）
  - `role_in_project`: 在项目中的角色（可选）

---

## 用户个人资料

### 1. 获取用户个人资料列表

```bash
curl -X GET "http://localhost:5000/api/v1/user-profiles?page=1&limit=10&gender=男&position=项目组长" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"items": [
			{
				"user_id": 1,
				"username": "admin",
				"full_name": "管理员",
				"gender": "男",
				"birth_date": "1995-06-15",
				"position": "项目组长",
				"dormitory": "2栋305室",
				"tech_stack": ["Python", "Vue.js", "MySQL"]
			}
		],
		"pagination": {
			"has_next": false,
			"has_prev": false,
			"limit": 10,
			"page": 1,
			"total": 1,
			"total_pages": 1
		}
	},
	"message": "获取用户个人资料列表成功",
	"success": true
}
```

### 2. 获取指定用户个人资料

```bash
curl -X GET "http://localhost:5000/api/v1/user-profiles/1" \
  -H "Content-Type: application/json"
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"user_id": 1,
		"username": "admin",
		"full_name": "管理员",
		"gender": "男",
		"birth_date": "1995-06-15",
		"position": "项目组长",
		"dormitory": "2栋305室",
		"tech_stack": ["Python", "Vue.js", "MySQL"]
	},
	"message": "获取用户个人资料成功",
	"success": true
}
```

### 3. 创建用户个人资料

```bash
curl -X POST "http://localhost:5000/api/v1/user-profiles" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "user_id": 2,
    "gender": "女",
    "birth_date": "1998-03-20",
    "position": "技术开发",
    "dormitory": "3栋201室",
    "tech_stack": ["Java", "React", "PostgreSQL"]
  }'
```

**响应示例:**
```json
{
	"code": 201,
	"data": {
		"user_id": 2,
		"username": "user2",
		"full_name": "用户2",
		"gender": "女",
		"birth_date": "1998-03-20",
		"position": "技术开发",
		"dormitory": "3栋201室",
		"tech_stack": ["Java", "React", "PostgreSQL"]
	},
	"message": "创建用户个人资料成功",
	"success": true
}
```

### 4. 更新用户个人资料

```bash
curl -X PUT "http://localhost:5000/api/v1/user-profiles/2" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "gender": "女",
    "birth_date": "1998-03-20",
    "position": "高级开发工程师",
    "dormitory": "3栋301室",
    "tech_stack": ["Java", "React", "PostgreSQL", "Docker"]
  }'
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"user_id": 2,
		"username": "user2",
		"full_name": "用户2",
		"gender": "女",
		"birth_date": "1998-03-20",
		"position": "高级开发工程师",
		"dormitory": "3栋301室",
		"tech_stack": ["Java", "React", "PostgreSQL", "Docker"]
	},
	"message": "更新用户个人资料成功",
	"success": true
}
```

### 5. 删除用户个人资料

```bash
curl -X DELETE "http://localhost:5000/api/v1/user-profiles/2" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"message": "删除用户个人资料成功",
	"success": true
}
```

### 6. 获取当前登录用户个人资料

```bash
curl -X GET "http://localhost:5000/api/v1/user-profiles/me" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"user_id": 1,
		"username": "admin",
		"full_name": "管理员",
		"gender": "男",
		"birth_date": "1995-06-15",
		"position": "项目组长",
		"dormitory": "2栋305室",
		"tech_stack": ["Python", "Vue.js", "MySQL"]
	},
	"message": "获取当前用户个人资料成功",
	"success": true
}
```

### 7. 更新当前登录用户个人资料

```bash
curl -X PUT "http://localhost:5000/api/v1/user-profiles/me" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "gender": "男",
    "birth_date": "1995-06-15",
    "position": "高级项目经理",
    "dormitory": "2栋405室",
    "tech_stack": ["Python", "Vue.js", "MySQL", "Redis", "Docker"]
  }'
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"user_id": 1,
		"username": "admin",
		"full_name": "管理员",
		"gender": "男",
		"birth_date": "1995-06-15",
		"position": "高级项目经理",
		"dormitory": "2栋405室",
		"tech_stack": ["Python", "Vue.js", "MySQL", "Redis", "Docker"]
	},
	"message": "更新当前用户个人资料成功",
	"success": true
}
```

**字段说明:**
- `user_id`: 用户ID（创建时必填，更新时不可修改）
- `gender`: 性别（可选，可选值：'男', '女', '保密'）
- `birth_date`: 出生日期（可选，格式：YYYY-MM-DD）
- `position`: 职务（可选，例如：项目组长、成员、2023级负责人）
- `dormitory`: 宿舍信息（可选，例如：2栋305室）
- `tech_stack`: 技术栈（可选，JSON数组格式）

---

## 环境监测

### 1. 获取环境监测日志列表

```bash
curl -X GET "http://localhost:5000/api/v1/environmental/data?page=1&limit=10&sensor_type=温度&lab_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"items": [
			{
				"id": 1,
				"sensor_type": "温度",
				"value": 23.5,
				"unit": "°C",
				"lab_id": 1,
				"timestamp": "2025-01-20T10:30:00"
			},
			{
				"id": 2,
				"sensor_type": "湿度",
				"value": 62.8,
				"unit": "%",
				"lab_id": 1,
				"timestamp": "2025-01-20T11:00:00"
			}
		],
		"pagination": {
			"has_next": true,
			"has_prev": false,
			"limit": 10,
			"page": 1,
			"total": 25,
			"total_pages": 3
		}
	},
	"message": "获取环境监测日志列表成功",
	"success": true
}
```

### 2. 创建环境监测日志

```bash
curl -X POST "http://localhost:5000/api/v1/environmental/data" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "sensor_type": "温度",
    "value": 25.3,
    "unit": "°C",
    "lab_id": 1
  }'
```

**响应示例:**
```json
{
	"code": 201,
	"data": {
		"id": 24,
		"lab_id": 1,
		"sensor_type": "温度",
		"timestamp": "2025-07-24T20:39:46",
		"unit": "°C",
		"value": 25.3
	},
	"message": "创建环境监测日志成功",
	"success": true
}
```

### 3. 获取单个环境监测日志详情

```bash
curl -X GET "http://localhost:5000/api/v1/environmental/data/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"id": 1,
		"sensor_type": "温度",
		"value": 23.5,
		"unit": "°C",
		"lab_id": 1,
		"timestamp": "2025-01-20T10:30:00"
	},
	"message": "获取环境监测日志详情成功",
	"success": true
}
```

### 4. 删除环境监测日志

```bash
curl -X DELETE "http://localhost:5000/api/v1/environmental/data/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"message": "删除环境监测日志成功",
	"success": true
}
```

### 5. 获取最新环境监测数据

```bash
curl -X GET "http://localhost:5000/api/v1/environmental/data/latest" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"CO2": {
			"id": 20,
			"lab_id": 1,
			"sensor_type": "CO2",
			"timestamp": "2025-07-24T12:00:00",
			"unit": "ppm",
			"value": 720
		},
		"光照": {
			"id": 19,
			"lab_id": 1,
			"sensor_type": "光照",
			"timestamp": "2025-07-24T12:00:00",
			"unit": "lux",
			"value": 790
		},
		"温度": {
			"id": 24,
			"lab_id": 1,
			"sensor_type": "温度",
			"timestamp": "2025-07-24T20:39:46",
			"unit": "°C",
			"value": 25.3
		},
		"湿度": {
			"id": 18,
			"lab_id": 1,
			"sensor_type": "湿度",
			"timestamp": "2025-07-24T12:00:00",
			"unit": "%",
			"value": 58
		}
	},
	"message": "获取最新环境监测数据成功",
	"success": true
}
```

### 6. 获取环境监测统计数据

```bash
curl -X GET "http://localhost:5000/api/v1/environmental/data/statistics?sensor_type=温度&hours=168" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例:**
```json
{
	"code": 200,
	"data": {
		"sensor_type": "温度",
		"period": "最近168小时",
		"total_records": 168,
		"statistics": {
			"avg": 24.2,
			"min": 20.5,
			"max": 27.8
		}
	},
	"message": "获取环境监测统计数据成功",
	"success": true
}
```

### 7. 批量创建环境监测日志

```bash
curl -X POST "http://localhost:5000/api/v1/environmental/data/batch" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '[
    {
      "sensor_type": "温度",
      "value": 23.8,
      "unit": "°C",
      "lab_id": 1
    },
    {
      "sensor_type": "湿度",
      "value": 66.2,
      "unit": "%",
      "lab_id": 1
    },
    {
      "sensor_type": "光照",
      "value": 322.5,
      "unit": "lux",
      "lab_id": 1
    }
  ]'
```

**响应示例:**
```json
{
	"code": 201,
	"data": [
		{
			"id": 27,
			"sensor_type": "温度",
			"value": 23.8,
			"unit": "°C",
			"lab_id": 1,
			"timestamp": "2025-01-22T15:00:00"
		},
		{
			"id": 28,
			"sensor_type": "湿度",
			"value": 66.2,
			"unit": "%",
			"lab_id": 1,
			"timestamp": "2025-01-22T15:00:00"
		},
		{
			"id": 29,
			"sensor_type": "光照",
			"value": 322.5,
			"unit": "lux",
			"lab_id": 1,
			"timestamp": "2025-01-22T15:00:00"
		}
	],
	"message": "批量创建3条环境监测日志成功",
	"success": true
}
```

**字段说明:**
- `sensor_type`: 传感器类型（必填，可选值：温度、湿度、光照、CO2）
- `value`: 监测数值（必填，浮点数）
- `unit`: 单位（必填，字符串）
- `lab_id`: 实验室ID（必填，整数）
- `timestamp`: 时间戳（可选，ISO格式，默认为当前北京时间）

**查询参数说明:**
- `page`: 页码（默认为1）
- `limit`: 每页数量（默认为10，最大100）
- `sensor_type`: 传感器类型筛选（可选）
- `lab_id`: 实验室ID筛选（可选）
- `start_time`: 开始时间（可选，ISO格式）
- `end_time`: 结束时间（可选，ISO格式）
- `hours`: 统计小时数（默认为24小时）

---

## 文件上传

## 1. 单个图片上传

### 接口信息

- **接口地址**: `POST /api/v1/upload/image`
- **认证方式**: JWT Token
- **请求类型**: multipart/form-data

### 测试用例

#### 1.1 正常上传测试

```bash
# 上传JPG图片
curl -X POST "http://localhost:5000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@test_image.jpg"
```

**预期响应**:

```json
{
  "code": 201,
  "success": true,
  "message": "文件上传成功",
  "data": {
    "filename": "550e8400-e29b-41d4-a716-446655440000.jpg",
    "original_filename": "test_image.jpg",
    "file_url": "/static/uploads/550e8400-e29b-41d4-a716-446655440000.jpg",
    "file_size": 1024000
  }
}
```

#### 1.2 不同格式图片测试

```bash
# 上传PNG图片
curl -X POST "http://localhost:5000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@test_image.png"

# 上传GIF图片
curl -X POST "http://localhost:5000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@test_image.gif"

# 上传WEBP图片
curl -X POST "http://localhost:5000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@test_image.webp"
```

---

## 2. 批量图片上传

### 接口信息

- **接口地址**: `POST /api/v1/upload/multiple`
- **认证方式**: JWT Token
- **请求类型**: multipart/form-data
- **文件数量限制**: 最多10个文件

### 测试用例

#### 2.1 批量上传多个图片

```bash
# 上传多个图片文件
curl -X POST "http://localhost:5000/api/v1/upload/multiple" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "files=@image1.jpg" \
  -F "files=@image2.png" \
  -F "files=@image3.gif"
```

**预期响应**:

```json
{
  "code": 200,
  "success": true,
  "message": "批量上传成功",
  "data": {
    "uploaded_files": [
      {
        "filename": "550e8400-e29b-41d4-a716-446655440001.jpg",
        "original_filename": "image1.jpg",
        "file_url": "/static/uploads/550e8400-e29b-41d4-a716-446655440001.jpg",
        "file_size": 1024000
      },
      {
        "filename": "550e8400-e29b-41d4-a716-446655440002.png",
        "original_filename": "image2.png",
        "file_url": "/static/uploads/550e8400-e29b-41d4-a716-446655440002.png",
        "file_size": 2048000
      }
    ],
    "total_uploaded": 2,
    "failed_files": []
  }
}
```

#### 2.2 批量上传边界测试（10个文件）

```bash
# 上传10个文件（最大限制）
curl -X POST "http://localhost:5000/api/v1/upload/multiple" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "files=@img1.jpg" \
  -F "files=@img2.jpg" \
  -F "files=@img3.jpg" \
  -F "files=@img4.jpg" \
  -F "files=@img5.jpg" \
  -F "files=@img6.jpg" \
  -F "files=@img7.jpg" \
  -F "files=@img8.jpg" \
  -F "files=@img9.jpg" \
  -F "files=@img10.jpg"
```

---

## 3. 获取上传配置

### 接口信息

- **接口地址**: `GET /api/v1/upload/info`
- **认证方式**: 无需认证
- **请求类型**: GET

### 测试用例

#### 3.1 获取上传配置信息

```bash
curl -X GET "http://localhost:5000/api/v1/upload/info"
```

**预期响应**:

```json
{
  "code": 200,
  "success": true,
  "message": "获取上传配置信息成功",
  "data": {
    "max_file_size": 5242880,
    "max_file_size_mb": 5.0,
    "allowed_extensions": ["jpg", "jpeg", "png", "gif", "bmp", "webp"],
    "upload_folder": "uploads"
  }
}
```

---

## 4. 测试注意事项

### 4.1 认证Token获取

在测试文件上传接口前，需要先获取JWT Token：

```bash
# 登录获取Token
curl -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

### 4.2 测试文件准备

建议准备以下测试文件：

- `test_image.jpg` (小于5MB的JPG图片)
- `test_image.png` (小于5MB的PNG图片)
- `test_image.gif` (小于5MB的GIF图片)
- `large_image.jpg` (大于5MB的图片，用于测试文件大小限制)
- `invalid_file.txt` (非图片文件，用于测试文件类型限制)

### 4.3 文件访问测试

上传成功后，可以通过以下方式访问文件：

```bash
# 访问上传的文件
curl -X GET "http://localhost:5000/static/uploads/FILENAME"
```

---

## 5. 错误处理测试

### 5.1 无认证测试

```bash
# 不提供Token
curl -X POST "http://localhost:5000/api/v1/upload/image" \
  -F "file=@test_image.jpg"
```

**预期响应**:

```json
{
  "msg": "Missing Authorization Header"
}
```

### 5.2 无效文件类型测试

```bash
# 上传非图片文件
curl -X POST "http://localhost:5000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@test_file.txt"
```

**预期响应**:

```json
{
  "code": 400,
  "success": false,
  "message": "不支持的文件类型，支持的类型: jpg, jpeg, png, gif, bmp, webp"
}
```

### 5.3 文件大小超限测试

```bash
# 上传大于5MB的文件
curl -X POST "http://localhost:5000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@large_image.jpg"
```

**预期响应**:

```json
{
  "code": 400,
  "success": false,
  "message": "文件大小超过限制，最大允许 5.0MB"
}
```

### 5.4 空文件测试

```bash
# 不选择文件
curl -X POST "http://localhost:5000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**预期响应**:

```json
{
  "code": 400,
  "success": false,
  "message": "没有选择文件"
}
```

### 5.5 批量上传超限测试

```bash
# 上传超过10个文件
curl -X POST "http://localhost:5000/api/v1/upload/multiple" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "files=@img1.jpg" \
  -F "files=@img2.jpg" \
  # ... 添加更多文件直到超过10个
```

---

## 测试脚本示例

### Python测试脚本

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件上传API测试脚本
"""

import requests
import json
from io import BytesIO
from PIL import Image

API_BASE_URL = "http://127.0.0.1:5000/api/v1"

def create_test_image(size=(100, 100), color='red', format='PNG'):
    """创建测试图片"""
    img = Image.new('RGB', size, color=color)
    img_bytes = BytesIO()
    img.save(img_bytes, format=format)
    img_bytes.seek(0)
    return img_bytes

def login():
    """登录获取Token"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data['data']['token']
    return None

def test_single_upload(token):
    """测试单个文件上传"""
    test_image = create_test_image()
    files = {'file': ('test_image.png', test_image, 'image/png')}
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(f"{API_BASE_URL}/upload/image", files=files, headers=headers)
    print(f"单个上传测试: {response.status_code}")
    print(f"响应: {response.text}")
    return response.status_code == 201

def test_multiple_upload(token):
    """测试批量文件上传"""
    files = []
    for i in range(3):
        test_image = create_test_image(color=['red', 'green', 'blue'][i])
        files.append(('files', (f'test_image_{i}.png', test_image, 'image/png')))
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f"{API_BASE_URL}/upload/multiple", files=files, headers=headers)
    print(f"批量上传测试: {response.status_code}")
    print(f"响应: {response.text}")
    return response.status_code == 200

def test_upload_info():
    """测试获取上传配置"""
    response = requests.get(f"{API_BASE_URL}/upload/info")
    print(f"上传配置测试: {response.status_code}")
    print(f"响应: {response.text}")
    return response.status_code == 200

def main():
    print("=== 文件上传API测试 ===")
    
    # 1. 获取Token
    token = login()
    if not token:
        print("❌ 登录失败")
        return
    
    # 2. 测试上传配置
    if test_upload_info():
        print("✅ 上传配置测试通过")
    else:
        print("❌ 上传配置测试失败")
    
    # 3. 测试单个上传
    if test_single_upload(token):
        print("✅ 单个上传测试通过")
    else:
        print("❌ 单个上传测试失败")
    
    # 4. 测试批量上传
    if test_multiple_upload(token):
        print("✅ 批量上传测试通过")
    else:
        print("❌ 批量上传测试失败")

if __name__ == "__main__":
    main()
```

---

## 支持的文件格式

- **JPG/JPEG**: 标准JPEG图片格式
- **PNG**: 支持透明度的PNG格式
- **GIF**: 支持动画的GIF格式
- **BMP**: Windows位图格式
- **WEBP**: Google开发的现代图片格式

## 文件大小限制

- **单个文件**: 最大5MB
- **批量上传**: 每个文件最大5MB，最多10个文件

## 安全说明

1. 所有上传接口都需要JWT认证
2. 文件名会被自动处理为安全格式
3. 生成唯一的UUID文件名防止冲突
4. 严格的文件类型和大小检查
5. 上传的文件存储在安全的目录中

---

**注意**: 请确保在测试前启动Flask应用服务器，并根据实际部署环境调整API基础URL。

---

## 注意事项

1. **JWT Token获取**: 首先调用登录接口获取JWT Token，然后在需要认证的接口中使用
2. **Token格式**: 在Authorization头中使用 `Bearer YOUR_JWT_TOKEN` 格式
3. **日期格式**: 所有日期字段使用 `YYYY-MM-DD` 格式
4. **时间格式**: 所有时间字段使用 `HH:MM` 格式
5. **分页参数**: `page` 从1开始，`limit` 建议不超过100
6. **状态值**: 请参考各接口的有效状态值列表
7. **必填字段**: 创建接口中标注的必填字段不能为空
8. **可选字段**: 即使是可选字段，在测试时也建议包含以确保完整性
9. **用户个人资料**: 用户个人资料与用户表通过user_id关联，删除用户时会级联删除个人资料


---

*文档生成时间: 2025年*
*适用版本: v1.0*