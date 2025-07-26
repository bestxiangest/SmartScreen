## 仓库物料管理

### 1. 获取物料列表

**接口地址**: `GET /api/v1/materials`

**描述**: 获取物料列表（分页）

**认证**: 需要JWT令牌

**查询参数**:

- `page` (int, 可选): 页码，默认1
- `limit` (int, 可选): 每页数量，默认10
- `category_id` (int, 可选): 物料分类ID筛选
- `keyword` (string, 可选): 关键词搜索（物料名称、编码）
- `status` (string, 可选): 物料状态筛选
- `location` (string, 可选): 存放位置筛选

**物料状态**:

- `available` - 可用
- `low_stock` - 库存不足
- `out_of_stock` - 缺货
- `reserved` - 已预留

**响应示例**:

```json
{
  "code": 200,
  "success": true,
  "message": "获取物料列表成功",
  "data": {
    "items": [
      {
        "id": 1,
        "code": "MAT001",
        "name": "Arduino开发板",
        "category_id": 1,
        "category_name": "电子元件",
        "description": "Arduino Uno R3开发板",
        "unit": "个",
        "stock_quantity": 25,
        "min_stock": 5,
        "max_stock": 50,
        "unit_price": 35.00,
        "location": "A区-01-03",
        "status": "available",
        "supplier": "电子科技有限公司",
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

### 2. 创建物料

**接口地址**: `POST /api/v1/materials`

**描述**: 创建新的物料

**认证**: 需要JWT令牌

**请求参数**:

```json
{
  "code": "MAT002",
  "name": "树莓派4B",
  "category_id": 1,
  "description": "树莓派4B 4GB内存版本",
  "unit": "个",
  "stock_quantity": 10,
  "min_stock": 2,
  "max_stock": 20,
  "unit_price": 450.00,
  "location": "A区-01-04",
  "supplier": "电子科技有限公司"
}
```

**参数说明**:

- `code` (string, 必填): 物料编码，唯一
- `name` (string, 必填): 物料名称
- `category_id` (int, 必填): 物料分类ID
- `description` (string, 可选): 物料描述
- `unit` (string, 必填): 计量单位
- `stock_quantity` (int, 必填): 库存数量
- `min_stock` (int, 可选): 最小库存
- `max_stock` (int, 可选): 最大库存
- `unit_price` (decimal, 可选): 单价
- `location` (string, 可选): 存放位置
- `supplier` (string, 可选): 供应商

**响应示例**: 同获取物料列表中的单个物料数据

### 3. 获取物料详情

**接口地址**: `GET /api/v1/materials/{material_id}`

**描述**: 获取指定物料详情

**认证**: 需要JWT令牌

**路径参数**:

- `material_id` (int, 必填): 物料ID

**响应示例**: 同创建物料的响应

### 4. 更新物料

**接口地址**: `PUT /api/v1/materials/{material_id}`

**描述**: 更新指定物料

**认证**: 需要JWT令牌

**路径参数**:

- `material_id` (int, 必填): 物料ID

**请求参数**: 同创建物料，所有字段均为可选

**响应示例**: 同获取物料详情

### 5. 删除物料

**接口地址**: `DELETE /api/v1/materials/{material_id}`

**描述**: 删除指定物料

**认证**: 需要JWT令牌

**路径参数**:

- `material_id` (int, 必填): 物料ID

**响应示例**:

```json
{
  "code": 200,
  "success": true,
  "message": "物料删除成功"
}
```

### 6. 获取物料分类列表

**接口地址**: `GET /api/v1/material-categories`

**描述**: 获取物料分类列表

**认证**: 需要JWT令牌

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
      "parent_id": null,
      "sort_order": 1,
      "created_at": "2024-01-15T10:00:00Z"
    },
    {
      "id": 2,
      "name": "机械零件",
      "description": "各类机械零部件",
      "parent_id": null,
      "sort_order": 2,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### 7. 创建物料分类

**接口地址**: `POST /api/v1/material-categories`

**描述**: 创建新的物料分类

**认证**: 需要JWT令牌

**请求参数**:

```json
{
  "name": "实验耗材",
  "description": "实验室常用耗材",
  "parent_id": null,
  "sort_order": 3
}
```

**参数说明**:

- `name` (string, 必填): 分类名称，唯一
- `description` (string, 可选): 分类描述
- `parent_id` (int, 可选): 父分类ID，用于创建子分类
- `sort_order` (int, 可选): 排序顺序，默认0

**响应示例**:

```json
{
  "code": 201,
  "success": true,
  "message": "创建物料分类成功",
  "data": {
    "id": 3,
    "name": "实验耗材",
    "description": "实验室常用耗材",
    "parent_id": null,
    "sort_order": 3,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

### 8. 更新物料分类

**接口地址**: `PUT /api/v1/material-categories/{category_id}`

**描述**: 更新指定物料分类

**认证**: 需要JWT令牌

**路径参数**:

- `category_id` (int, 必填): 分类ID

**请求参数**: 同创建物料分类，所有字段均为可选

**响应示例**:

```json
{
  "code": 200,
  "success": true,
  "message": "更新物料分类成功",
  "data": {
    "id": 3,
    "name": "实验耗材（更新）",
    "description": "实验室常用耗材和工具",
    "parent_id": null,
    "sort_order": 3,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  }
}
```

### 9. 删除物料分类

**接口地址**: `DELETE /api/v1/material-categories/{category_id}`

**描述**: 删除指定物料分类

**认证**: 需要JWT令牌

**路径参数**:

- `category_id` (int, 必填): 分类ID

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
  "message": "该分类下存在子分类，无法删除"
}
```

```json
{
  "code": 400,
  "success": false,
  "message": "该分类下存在物料，无法删除"
}
```

### 10. 物料申领

**接口地址**: `POST /api/v1/material-requests`

**描述**: 创建物料申领申请

**认证**: 需要JWT令牌

**请求参数**:

```json
{
  "materials": [
    {
      "material_id": 1,
      "quantity": 2,
      "purpose": "项目制作"
    },
    {
      "material_id": 2,
      "quantity": 1,
      "purpose": "实验使用"
    }
  ],
  "project_name": "智能家居系统",
  "expected_return_date": "2024-02-15",
  "notes": "用于期末项目制作"
}
```

**参数说明**:

- `materials` (array, 必填): 申领物料列表
    - `material_id` (int, 必填): 物料ID
    - `quantity` (int, 必填): 申领数量
    - `purpose` (string, 可选): 使用目的
- `project_name` (string, 可选): 项目名称
- `expected_return_date` (string, 可选): 预期归还日期，格式YYYY-MM-DD
- `notes` (string, 可选): 备注

**响应示例**:

```json
{
  "code": 201,
  "success": true,
  "message": "物料申领申请创建成功",
  "data": {
    "id": 1,
    "request_number": "REQ202401150001",
    "user_id": 1,
    "user_name": "张三",
    "project_name": "智能家居系统",
    "status": "pending",
    "expected_return_date": "2024-02-15",
    "notes": "用于期末项目制作",
    "materials": [
      {
        "material_id": 1,
        "material_name": "Arduino开发板",
        "quantity": 2,
        "purpose": "项目制作"
      }
    ],
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

### 8. 获取物料申领列表

**接口地址**: `GET /api/v1/material-requests`

**描述**: 获取物料申领列表（分页）

**认证**: 需要JWT令牌

**查询参数**:

- `page` (int, 可选): 页码，默认1
- `limit` (int, 可选): 每页数量，默认10
- `status` (string, 可选): 申领状态筛选
- `user_id` (int, 可选): 用户ID筛选

**申领状态**:

- `pending` - 待审核
- `approved` - 已批准
- `rejected` - 已拒绝
- `issued` - 已发放
- `returned` - 已归还
- `overdue` - 逾期未还

**响应示例**: 同物料申领的响应，包含分页信息

### 9. 审批物料申领

**接口地址**: `PUT /api/v1/material-requests/{request_id}/approve`

**描述**: 审批物料申领申请

**认证**: 需要JWT令牌

**路径参数**:

- `request_id` (int, 必填): 申领ID

**请求参数**:

```json
{
  "action": "approve",
  "comment": "审批通过",
  "approved_materials": [
    {
      "material_id": 1,
      "approved_quantity": 2
    }
  ]
}
```

**参数说明**:

- `action` (string, 必填): 审批动作，可选值：approve（批准）、reject（拒绝）
- `comment` (string, 可选): 审批意见
- `approved_materials` (array, 可选): 批准的物料列表（仅在批准时需要）

### 10. 物料出入库记录

**接口地址**: `GET /api/v1/material-transactions`

**描述**: 获取物料出入库记录

**认证**: 需要JWT令牌

**查询参数**:

- `page` (int, 可选): 页码，默认1
- `limit` (int, 可选): 每页数量，默认10
- `material_id` (int, 可选): 物料ID筛选
- `transaction_type` (string, 可选): 交易类型筛选
- `start_date` (string, 可选): 开始日期，格式YYYY-MM-DD
- `end_date` (string, 可选): 结束日期，格式YYYY-MM-DD

**交易类型**:

- `in` - 入库
- `out` - 出库
- `return` - 归还
- `adjust` - 调整

**响应示例**:

```json
{
  "code": 200,
  "success": true,
  "message": "获取物料出入库记录成功",
  "data": {
    "items": [
      {
        "id": 1,
        "material_id": 1,
        "material_name": "Arduino开发板",
        "transaction_type": "out",
        "quantity": 2,
        "before_quantity": 25,
        "after_quantity": 23,
        "user_id": 1,
        "user_name": "张三",
        "request_id": 1,
        "notes": "项目制作申领",
        "created_at": "2024-01-15T10:00:00Z"
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

### 11. 库存统计

**接口地址**: `GET /api/v1/materials/statistics`

**描述**: 获取库存统计数据

**认证**: 需要JWT令牌

**查询参数**:

- `period` (string, 可选): 统计周期，可选值：day、week、month
- `category_id` (int, 可选): 物料分类ID筛选

**响应示例**:

```json
{
  "code": 200,
  "success": true,
  "message": "获取库存统计成功",
  "data": {
    "total_materials": 150,
    "total_value": 45000.00,
    "low_stock_count": 8,
    "out_of_stock_count": 3,
    "daily_out": 25,
    "weekly_out": 180,
    "monthly_out": 720,
    "top_requested_materials": [
      {
        "material_id": 1,
        "material_name": "Arduino开发板",
        "request_count": 15
      },
      {
        "material_id": 2,
        "material_name": "树莓派4B",
        "request_count": 12
      }
    ],
    "category_distribution": [
      {
        "category_id": 1,
        "category_name": "电子元件",
        "material_count": 85,
        "total_value": 28000.00
      },
      {
        "category_id": 2,
        "category_name": "机械零件",
        "material_count": 65,
        "total_value": 17000.00
      }
    ]
  }
}
```

---

## 维修工单管理

### 1. 获取维修工单列表

**接口地址**: `GET /api/v1/maintenance-orders`

**描述**: 获取维修工单列表（分页）

**认证**: 需要JWT令牌

**查询参数**:

- `page` (int, 可选): 页码，默认1
- `limit` (int, 可选): 每页数量，默认10
- `device_id` (int, 可选): 设备ID筛选
- `status` (string, 可选): 工单状态筛选
- `priority` (string, 可选): 优先级筛选
- `fault_type` (string, 可选): 故障类型筛选
- `reporter_id` (int, 可选): 报修人ID筛选
- `assignee_id` (int, 可选): 维修人员ID筛选

**工单状态**:

- `pending` - 待处理
- `assigned` - 已分配
- `in_progress` - 处理中
- `completed` - 已完成
- `cancelled` - 已取消

**优先级**:

- `low` - 低
- `medium` - 中
- `high` - 高
- `urgent` - 紧急

**故障类型**:

- `hardware` - 硬件故障
- `software` - 软件故障
- `network` - 网络故障
- `power` - 电源故障
- `other` - 其他

**响应示例**:

```json
{
  "code": 200,
  "success": true,
  "message": "获取维修工单列表成功",
  "data": {
    "items": [
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
          "http://localhost:5000/uploads/fault_image1.jpg"
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

### 2. 创建维修工单

**接口地址**: `POST /api/v1/maintenance-orders`

**描述**: 创建新的维修工单（故障报修）

**认证**: 需要JWT令牌

**请求参数**:

```json
{
  "device_id": 1,
  "fault_type": "hardware",
  "fault_description": "激光头无法正常工作，切割效果异常",
  "priority": "high",
  "images": [
    "http://localhost:5000/uploads/fault_image1.jpg",
    "http://localhost:5000/uploads/fault_image2.jpg"
  ]
}
```

**参数说明**:

- `device_id` (int, 必填): 设备ID
- `fault_type` (string, 必填): 故障类型
- `fault_description` (string, 必填): 故障描述
- `priority` (string, 可选): 优先级，默认medium
- `images` (array, 可选): 故障图片URL列表

**响应示例**:

```json
{
  "code": 201,
  "success": true,
  "message": "维修工单创建成功",
  "data": {
    "id": 2,
    "order_number": "MO202401150002",
    "device_id": 1,
    "device_name": "激光切割机",
    "fault_type": "hardware",
    "fault_description": "激光头无法正常工作，切割效果异常",
    "priority": "high",
    "status": "pending",
    "reporter_id": 1,
    "reporter_name": "张三",
    "assignee_id": null,
    "assignee_name": null,
    "reported_at": "2024-01-15T10:00:00Z",
    "assigned_at": null,
    "expected_completion": null,
    "actual_completion": null,
    "images": [
      "http://localhost:5000/uploads/fault_image1.jpg",
      "http://localhost:5000/uploads/fault_image2.jpg"
    ],
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

### 3. 获取维修工单详情

**接口地址**: `GET /api/v1/maintenance-orders/{order_id}`

**描述**: 获取指定维修工单详情

**认证**: 需要JWT令牌

**路径参数**:

- `order_id` (int, 必填): 工单ID

**响应示例**: 同创建维修工单的响应，包含维修记录

### 4. 更新维修工单

**接口地址**: `PUT /api/v1/maintenance-orders/{order_id}`

**描述**: 更新指定维修工单

**认证**: 需要JWT令牌

**路径参数**:

- `order_id` (int, 必填): 工单ID

**请求参数**: 同创建维修工单，所有字段均为可选，另外可包含：

- `status` (string, 可选): 工单状态
- `assignee_id` (int, 可选): 维修人员ID
- `expected_completion` (string, 可选): 预期完成时间
- `maintenance_notes` (string, 可选): 维修备注

**响应示例**: 同获取维修工单详情

### 5. 分配维修工单

**接口地址**: `PUT /api/v1/maintenance-orders/{order_id}/assign`

**描述**: 分配维修工单给维修人员

**认证**: 需要JWT令牌

**路径参数**:

- `order_id` (int, 必填): 工单ID

**请求参数**:

```json
{
  "assignee_id": 2,
  "expected_completion": "2024-01-16T17:00:00Z",
  "notes": "请优先处理此工单"
}
```

**参数说明**:

- `assignee_id` (int, 必填): 维修人员ID
- `expected_completion` (string, 可选): 预期完成时间
- `notes` (string, 可选): 分配备注

### 6. 完成维修工单

**接口地址**: `PUT /api/v1/maintenance-orders/{order_id}/complete`

**描述**: 完成维修工单

**认证**: 需要JWT令牌

**路径参数**:

- `order_id` (int, 必填): 工单ID

**请求参数**:

```json
{
  "solution_description": "更换了激光头模块，重新校准了设备",
  "maintenance_notes": "建议定期清洁激光头",
  "completion_images": [
    "http://localhost:5000/uploads/repair_complete1.jpg"
  ],
  "parts_used": [
    {
      "part_name": "激光头模块",
      "quantity": 1,
      "cost": 500.00
    }
  ]
}
```

**参数说明**:

- `solution_description` (string, 必填): 解决方案描述
- `maintenance_notes` (string, 可选): 维修备注
- `completion_images` (array, 可选): 完成后的图片
- `parts_used` (array, 可选): 使用的零件列表

### 7. 获取维修统计

**接口地址**: `GET /api/v1/maintenance-orders/statistics`

**描述**: 获取维修工单统计数据

**认证**: 需要JWT令牌

**查询参数**:

- `start_date` (string, 可选): 开始日期，格式YYYY-MM-DD
- `end_date` (string, 可选): 结束日期，格式YYYY-MM-DD
- `device_id` (int, 可选): 设备ID筛选

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

## 值班调度管理

### 1. 获取值班安排列表

**接口地址**: `GET /api/v1/duty-schedules`

**描述**: 获取值班安排列表

**认证**: 需要JWT令牌

**查询参数**:

- `year` (int, 可选): 年份，默认当前年
- `month` (int, 可选): 月份，默认当前月
- `user_id` (int, 可选): 用户ID筛选
- `status` (string, 可选): 值班状态筛选

**值班状态**:

- `scheduled` - 已安排
- `completed` - 已完成
- `absent` - 缺勤
- `leave` - 请假
- `substituted` - 已替班

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

### 2. 创建值班安排

**接口地址**: `POST /api/v1/duty-schedules`

**描述**: 创建新的值班安排

**认证**: 需要JWT令牌

**请求参数**:

```json
{
  "user_id": 1,
  "duty_date": "2024-01-20",
  "shift_type": "afternoon",
  "start_time": "13:00",
  "end_time": "17:00",
  "location": "实验室B",
  "responsibilities": ["设备维护", "实验指导"],
  "notes": "新设备调试期间需要特别关注"
}
```

**参数说明**:

- `user_id` (int, 必填): 值班人员ID
- `duty_date` (string, 必填): 值班日期，格式YYYY-MM-DD
- `shift_type` (string, 必填): 班次类型（morning/afternoon/evening/night）
- `start_time` (string, 必填): 开始时间，格式HH:MM
- `end_time` (string, 必填): 结束时间，格式HH:MM
- `location` (string, 可选): 值班地点
- `responsibilities` (array, 可选): 职责列表
- `notes` (string, 可选): 备注

**响应示例**: 同获取值班安排列表中的单个数据

### 3. 更新值班安排

**接口地址**: `PUT /api/v1/duty-schedules/{schedule_id}`

**描述**: 更新指定值班安排

**认证**: 需要JWT令牌

**路径参数**:

- `schedule_id` (int, 必填): 值班安排ID

**请求参数**: 同创建值班安排，所有字段均为可选

### 4. 删除值班安排

**接口地址**: `DELETE /api/v1/duty-schedules/{schedule_id}`

**描述**: 删除指定值班安排

**认证**: 需要JWT令牌

**路径参数**:

- `schedule_id` (int, 必填): 值班安排ID

### 5. 申请替班

**接口地址**: `POST /api/v1/duty-schedules/{schedule_id}/substitute`

**描述**: 申请替班

**认证**: 需要JWT令牌

**路径参数**:

- `schedule_id` (int, 必填): 值班安排ID

**请求参数**:

```json
{
  "substitute_id": 2,
  "reason": "临时有事，需要请假",
  "notes": "已与替班人员沟通确认"
}
```

**参数说明**:

- `substitute_id` (int, 必填): 替班人员ID
- `reason` (string, 必填): 替班原因
- `notes` (string, 可选): 备注

### 6. 值班签到

**接口地址**: `POST /api/v1/duty-schedules/{schedule_id}/check-in`

**描述**: 值班签到

**认证**: 需要JWT令牌

**路径参数**:

- `schedule_id` (int, 必填): 值班安排ID

**请求参数**:

```json
{
  "check_in_time": "2024-01-15T08:00:00Z",
  "location": "实验室A",
  "notes": "准时到岗，设备状态正常"
}
```

### 7. 值班签退

**接口地址**: `POST /api/v1/duty-schedules/{schedule_id}/check-out`

**描述**: 值班签退

**认证**: 需要JWT令牌

**路径参数**:

- `schedule_id` (int, 必填): 值班安排ID

**请求参数**:

```json
{
  "check_out_time": "2024-01-15T12:00:00Z",
  "summary": "值班期间无异常，完成设备巡检",
  "issues": [],
  "handover_notes": "下班次需要关注3D打印机耗材"
}
```

### 8. 获取值班统计

**接口地址**: `GET /api/v1/duty-schedules/statistics`

**描述**: 获取值班统计数据

**认证**: 需要JWT令牌

**查询参数**:

- `year` (int, 可选): 年份
- `month` (int, 可选): 月份
- `user_id` (int, 可选): 用户ID筛选

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

