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
4. [通知公告](#通知公告)
5. [考勤管理](#考勤管理)
6. [实验室信息](#实验室信息)
7. [设备管理](#设备管理)
8. [课程表管理](#课程表管理)
9. [安全须知](#安全须知)
10. [项目成果](#项目成果)

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
curl -X GET "http://localhost:5000/api/v1/attendance?page=1&limit=10&user_id=1&date=2024-01-15&method=人脸识别" \
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
curl -X GET "http://localhost:5000/api/v1/attendance/statistics?user_id=1&start_date=2024-01-01&end_date=2024-01-31" \
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
    "user_id": 1,
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
    "user_id": 1
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

## 注意事项

1. **JWT Token获取**: 首先调用登录接口获取JWT Token，然后在需要认证的接口中使用
2. **Token格式**: 在Authorization头中使用 `Bearer YOUR_JWT_TOKEN` 格式
3. **日期格式**: 所有日期字段使用 `YYYY-MM-DD` 格式
4. **时间格式**: 所有时间字段使用 `HH:MM` 格式
5. **分页参数**: `page` 从1开始，`limit` 建议不超过100
6. **状态值**: 请参考各接口的有效状态值列表
7. **必填字段**: 创建接口中标注的必填字段不能为空
8. **可选字段**: 即使是可选字段，在测试时也建议包含以确保完整性


---

*文档生成时间: 2025年*
*适用版本: v1.0*