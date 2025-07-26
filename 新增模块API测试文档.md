# 新增模块API测试文档

本文档包含智慧实验室电子班牌系统新增三个模块的API接口测试命令和示例。

## 基础信息

- **服务器地址**: http://sys.sharpcaterpillar.top:5000
- **API版本**: v1
- **认证方式**: JWT Bearer Token
- **内容类型**: application/json

## 获取认证令牌

在测试新增模块API之前，需要先获取JWT令牌：

```bash
# 用户登录获取令牌
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password"
  }'
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "登录成功",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com"
    }
  }
}
```

**注意**: 将返回的 `access_token` 用于后续API调用的Authorization头。

---

## 仓库物料管理模块

### 1. 物料分类管理

#### 1.1 获取物料分类列表

```bash
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/material-categories" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "获取物料分类列表成功",
  "data": [
    {
      "id": 1,
      "name": "电子元件",
      "description": "各类电子元器件",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

#### 1.2 创建物料分类

```bash
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/material-categories \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "实验耗材",
    "description": "实验室常用耗材"
  }'
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "创建物料分类成功",
  "data": {
    "id": 2,
    "name": "实验耗材",
    "description": "实验室常用耗材",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 1.3 更新物料分类

```bash
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/material-categories/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "电子元件（更新）",
    "description": "各类电子元器件和传感器"
  }'
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "更新物料分类成功",
  "data": {
    "id": 1,
    "name": "电子元件（更新）",
    "description": "各类电子元器件和传感器",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  }
}
```

#### 1.4 删除物料分类

```bash
curl -X DELETE http://sys.sharpcaterpillar.top:5000/api/v1/material-categories/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "删除物料分类成功"
}
```

**错误响应示例**:
```json
{
  "code": 400,
  "success": false,
  "message": "该分类下存在物料，无法删除"
}
```

### 2. 物料管理

#### 2.1 获取物料列表

```bash
# 获取所有物料
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/materials" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按分类筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/materials?category_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按库存状态筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/materials?stock_status=low" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 分页查询
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/materials?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "获取物料列表成功",
  "data": {
    "materials": [
      {
        "id": 1,
        "name": "Arduino Uno R3",
        "code": "ARD-UNO-001",
        "category_id": 1,
        "category_name": "电子元件",
        "specification": "ATmega328P微控制器开发板",
        "unit": "个",
        "current_stock": 25,
        "min_stock": 10,
        "max_stock": 100,
        "unit_price": 35.00,
        "supplier": "深圳电子科技有限公司",
        "storage_location": "A区-1层-001",
        "status": "normal",
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
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

#### 2.2 创建物料

```bash
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/materials \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "树莓派4B",
    "code": "RPI-4B-001",
    "category_id": 1,
    "specification": "4GB RAM版本",
    "unit": "个",
    "current_stock": 15,
    "min_stock": 5,
    "max_stock": 50,
    "unit_price": 299.00,
    "supplier": "树莓派官方代理商",
    "storage_location": "A区-1层-002"
  }'
```

#### 2.3 获取物料详情

```bash
curl -X GET http://sys.sharpcaterpillar.top:5000/api/v1/materials/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

#### 2.4 更新物料信息

```bash
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/materials/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_stock": 30,
    "unit_price": 32.00,
    "storage_location": "A区-2层-001"
  }'
```

#### 2.5 批量更新物料库存

```bash
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/materials/batch-update-stock \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "updates": [
      {
        "material_id": 1,
        "stock_quantity": 50,
        "notes": "采购入库"
      },
      {
        "material_id": 2,
        "stock_quantity": 25,
        "notes": "盘点调整"
      }
    ]
  }'
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "批量更新物料库存成功",
  "data": {
    "updated_count": 2,
    "failed_count": 0,
    "results": [
      {
        "material_id": 1,
        "success": true,
        "message": "更新成功"
      },
      {
        "material_id": 2,
        "success": true,
        "message": "更新成功"
      }
    ]
  }
}
```

#### 2.6 删除物料

```bash
curl -X DELETE http://sys.sharpcaterpillar.top:5000/api/v1/materials/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. 物料申领管理

#### 3.1 获取申领列表

```bash
# 获取所有申领记录
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/material-requests" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按状态筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/material-requests?status=pending" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按申请人筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/material-requests?requester_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

#### 3.2 创建物料申领

```bash
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/material-requests \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "material_id": 1,
    "quantity": 5,
    "purpose": "智能家居项目开发",
    "expected_return_date": "2024-02-15",
    "notes": "用于学生课程设计"
  }'
```

#### 3.3 审批物料申领

```bash
# 批准申领
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/material-requests/1/approve \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "approved_quantity": 5,
    "notes": "申领理由合理，批准发放"
  }'

# 拒绝申领
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/material-requests/1/reject \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "库存不足，建议延后申领"
  }'
```

#### 3.4 完成物料申领

```bash
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/material-requests/1/complete \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "actual_quantity": 5,
    "notes": "物料已发放完毕"
  }'
```

### 4. 物料出入库记录

#### 4.1 获取出入库记录

```bash
# 获取所有记录
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/material-transactions" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按物料筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/material-transactions?material_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按交易类型筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/material-transactions?transaction_type=out" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按日期范围筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/material-transactions?start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

#### 4.2 创建出入库记录

```bash
# 入库记录
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/material-transactions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "material_id": 1,
    "transaction_type": "in",
    "quantity": 20,
    "unit_price": 35.00,
    "supplier": "深圳电子科技有限公司",
    "notes": "新采购入库"
  }'

# 出库记录
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/material-transactions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "material_id": 1,
    "transaction_type": "out",
    "quantity": 5,
    "recipient": "张三",
    "purpose": "课程实验使用",
    "notes": "学生申领"
  }'
```

### 5. 库存统计

#### 5.1 获取库存统计

```bash
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/materials/inventory-statistics" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "获取库存统计成功",
  "data": {
    "total_materials": 150,
    "total_value": 45000.00,
    "low_stock_materials": 8,
    "out_of_stock_materials": 2,
    "category_statistics": [
      {
        "category_id": 1,
        "category_name": "电子元件",
        "material_count": 50,
        "total_value": 15000.00
      }
    ],
    "recent_transactions": [
      {
        "id": 1,
        "material_name": "Arduino Uno R3",
        "transaction_type": "out",
        "quantity": 5,
        "transaction_date": "2024-01-15T14:30:00Z"
      }
    ]
  }
}
```

---

## 维修工单管理模块

### 1. 维修工单管理

#### 1.1 获取维修工单列表

```bash
# 获取所有工单
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按状态筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders?status=pending" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按设备筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders?device_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按优先级筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders?priority=high" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 分页查询
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "获取维修工单列表成功",
  "data": {
    "orders": [
      {
        "id": 1,
        "order_number": "MO202401150001",
        "device_id": 1,
        "device_name": "激光切割机",
        "fault_type": "hardware",
        "fault_description": "激光头无法正常工作",
        "priority": "high",
        "status": "in_progress",
        "reporter_id": 1,
        "reporter_name": "张三",
        "assignee_id": 2,
        "assignee_name": "李维修",
        "reported_at": "2024-01-15T09:00:00Z",
        "assigned_at": "2024-01-15T09:30:00Z",
        "expected_completion": "2024-01-16T17:00:00Z",
        "actual_completion": null,
        "images": [
          "http://sys.sharpcaterpillar.top:5000/uploads/fault_image1.jpg"
        ],
        "created_at": "2024-01-15T09:00:00Z",
        "updated_at": "2024-01-15T09:30:00Z"
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

#### 1.2 创建维修工单

```bash
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": 1,
    "fault_type": "hardware",
    "fault_description": "激光头无法正常工作，切割效果异常",
    "priority": "high",
    "images": [
      "http://sys.sharpcaterpillar.top:5000/uploads/fault_image1.jpg",
      "http://sys.sharpcaterpillar.top:5000/uploads/fault_image2.jpg"
    ]
  }'
```

#### 1.3 获取维修工单详情

```bash
curl -X GET http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

#### 1.4 更新维修工单

```bash
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fault_description": "激光头模块故障，需要更换",
    "priority": "urgent",
    "expected_completion": "2024-01-16T12:00:00Z",
    "maintenance_notes": "已联系供应商，零件明天到货"
  }'
```

#### 1.5 分配维修工单

```bash
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders/1/assign \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assignee_id": 2,
    "expected_completion": "2024-01-16T17:00:00Z",
    "notes": "请优先处理此工单"
  }'
```

#### 1.6 完成维修工单

```bash
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders/1/complete \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "solution_description": "更换了激光头模块，重新校准了设备",
    "maintenance_notes": "建议定期清洁激光头",
    "completion_images": [
      "http://sys.sharpcaterpillar.top:5000/uploads/repair_complete1.jpg"
    ],
    "parts_used": [
      {
        "part_name": "激光头模块",
        "quantity": 1,
        "cost": 500.00
      }
    ]
  }'
```

#### 1.7 删除维修工单

```bash
curl -X DELETE http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 2. 维修统计

#### 2.1 获取维修统计

```bash
# 获取总体统计
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders/statistics" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按日期范围统计
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders/statistics?start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按设备统计
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/maintenance-orders/statistics?device_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "获取维修统计成功",
  "data": {
    "total_orders": 45,
    "pending_orders": 8,
    "in_progress_orders": 12,
    "completed_orders": 23,
    "cancelled_orders": 2,
    "average_response_time": 2.5,
    "average_completion_time": 24.8,
    "this_week_orders": 12,
    "this_month_orders": 45,
    "fault_type_distribution": [
      {
        "fault_type": "hardware",
        "count": 20,
        "percentage": 44.4
      },
      {
        "fault_type": "software",
        "count": 15,
        "percentage": 33.3
      }
    ],
    "top_faulty_devices": [
      {
        "device_id": 1,
        "device_name": "激光切割机",
        "fault_count": 8
      },
      {
        "device_id": 2,
        "device_name": "3D打印机",
        "fault_count": 6
      }
    ]
  }
}
```

---

## 值班调度管理模块

### 1. 值班安排管理

#### 1.1 获取值班安排列表

```bash
# 获取当前月份值班安排
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按年月筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules?year=2024&month=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按用户筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules?user_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按状态筛选
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules?status=scheduled" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "获取值班安排列表成功",
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "user_name": "张三",
      "duty_date": "2024-01-15",
      "shift_type": "morning",
      "start_time": "08:00",
      "end_time": "12:00",
      "status": "scheduled",
      "location": "实验室A",
      "responsibilities": ["设备巡检", "安全监督", "学生指导"],
      "substitute_id": null,
      "substitute_name": null,
      "notes": "重点关注激光切割机运行状态",
      "created_at": "2024-01-10T10:00:00Z",
      "updated_at": "2024-01-10T10:00:00Z"
    }
  ]
}
```

#### 1.2 创建值班安排

```bash
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "duty_date": "2024-01-20",
    "shift_type": "afternoon",
    "start_time": "13:00",
    "end_time": "17:00",
    "location": "实验室B",
    "responsibilities": ["设备维护", "实验指导"],
    "notes": "新设备调试期间需要特别关注"
  }'
```

#### 1.3 获取值班安排详情

```bash
curl -X GET http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

#### 1.4 更新值班安排

```bash
curl -X PUT http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_time": "08:30",
    "end_time": "12:30",
    "location": "实验室A+B",
    "notes": "需要同时监管两个实验室"
  }'
```

#### 1.5 删除值班安排

```bash
curl -X DELETE http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 2. 替班管理

#### 2.1 申请替班

```bash
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/1/substitute \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "substitute_id": 2,
    "reason": "临时有事，需要请假",
    "notes": "已与替班人员沟通确认"
  }'
```

### 3. 值班签到签退

#### 3.1 值班签到

```bash
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/1/check-in \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "check_in_time": "2024-01-15T08:00:00Z",
    "location": "实验室A",
    "notes": "准时到岗，设备状态正常"
  }'
```

#### 3.2 值班签退

```bash
curl -X POST http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/1/check-out \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "check_out_time": "2024-01-15T12:00:00Z",
    "summary": "值班期间无异常，完成设备巡检",
    "issues": [],
    "handover_notes": "下班次需要关注3D打印机耗材"
  }'
```

### 4. 值班日历

#### 4.1 获取值班日历

```bash
# 获取当前月份日历
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/calendar" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 获取指定月份日历
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/calendar?year=2024&month=2" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

### 5. 值班统计

#### 5.1 获取值班统计

```bash
# 获取总体统计
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/statistics" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按年月统计
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/statistics?year=2024&month=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# 按用户统计
curl -X GET "http://sys.sharpcaterpillar.top:5000/api/v1/duty-schedules/statistics?user_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "code": 200,
  "success": true,
  "message": "获取值班统计成功",
  "data": {
    "total_schedules": 120,
    "completed_schedules": 110,
    "absent_schedules": 5,
    "leave_schedules": 3,
    "substituted_schedules": 2,
    "attendance_rate": 91.7,
    "user_statistics": [
      {
        "user_id": 1,
        "user_name": "张三",
        "total_duties": 20,
        "completed_duties": 19,
        "absent_duties": 1,
        "attendance_rate": 95.0
      }
    ],
    "monthly_distribution": [
      {
        "month": "2024-01",
        "total_schedules": 30,
        "completed_schedules": 28
      }
    ]
  }
}
```

---

## 常见错误响应

### 401 未授权
```json
{
  "code": 401,
  "success": false,
  "message": "Missing Authorization Header"
}
```

### 403 权限不足
```json
{
  "code": 403,
  "success": false,
  "message": "权限不足"
}
```

### 404 资源不存在
```json
{
  "code": 404,
  "success": false,
  "message": "资源不存在"
}
```

### 422 参数验证失败
```json
{
  "code": 422,
  "success": false,
  "message": "参数验证失败",
  "errors": {
    "name": ["名称不能为空"]
  }
}
```

### 500 服务器内部错误
```json
{
  "code": 500,
  "success": false,
  "message": "服务器内部错误"
}
```

---

## 注意事项

1. **认证令牌**: 所有API调用都需要在请求头中包含有效的JWT令牌
2. **内容类型**: POST和PUT请求需要设置`Content-Type: application/json`
3. **日期格式**: 日期参数使用ISO 8601格式（YYYY-MM-DDTHH:MM:SSZ）
4. **分页**: 列表接口支持分页，使用`page`和`limit`参数
5. **筛选**: 大部分列表接口支持多种筛选条件
6. **文件上传**: 图片等文件需要先通过文件上传接口上传，然后使用返回的URL
7. **权限控制**: 不同角色的用户对API的访问权限可能不同
8. **数据验证**: 请求参数会进行严格的数据验证，确保数据的完整性和安全性

---

## 测试建议

1. **环境准备**: 确保服务器正常运行，数据库连接正常
2. **认证测试**: 先测试登录接口，获取有效的JWT令牌
3. **基础功能**: 按照创建→查询→更新→删除的顺序测试基础CRUD功能
4. **业务流程**: 测试完整的业务流程，如物料申领审批流程、维修工单处理流程等
5. **边界条件**: 测试各种边界条件和异常情况
6. **性能测试**: 对于列表接口，测试大数据量下的性能表现
7. **权限测试**: 使用不同角色的用户测试权限控制是否正确