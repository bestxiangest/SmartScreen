# 智慧实验室电子班牌系统 - 文件上传API测试文档

本文档包含文件上传相关API接口的详细测试用例，包括curl命令、响应示例和测试说明。

## 目录
- [1. 单个图片上传](#1-单个图片上传)
- [2. 批量图片上传](#2-批量图片上传)
- [3. 获取上传配置](#3-获取上传配置)
- [4. 测试注意事项](#4-测试注意事项)
- [5. 错误处理测试](#5-错误处理测试)

---

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