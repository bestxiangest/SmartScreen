# 签到二维码生成 API 详细说明文档

## 概述

本文档详细说明了智慧实验室考勤系统中签到二维码生成相关的 API 接口，帮助开发人员在其他界面中集成二维码签到功能。

## 目录

1. [基础信息](#基础信息)
2. [API 接口列表](#api-接口列表)
3. [详细接口说明](#详细接口说明)
4. [前端集成示例](#前端集成示例)
5. [错误处理](#错误处理)
6. [安全说明](#安全说明)

## 基础信息

- **基础URL**: `http://localhost:5000/api/v1`
- **数据格式**: JSON
- **字符编码**: UTF-8
- **二维码有效期**: 当日23:59:59
- **Token算法**: SHA256哈希（前16位）

## API 接口列表

| 接口名称 | 方法 | 路径 | 认证 | 描述 |
|---------|------|------|------|------|
| 生成每日二维码 | GET | `/attendance/qr-code` | 否 | 生成包含当日token的二维码数据 |
| 生成URL二维码 | POST | `/attendance/qr-code-url` | 否 | 根据URL生成二维码图片 |
| 二维码签到 | POST | `/attendance/qr-checkin` | 否 | 通过二维码进行签到 |

## 详细接口说明

### 1. 生成每日二维码

**接口地址**: `GET /api/v1/attendance/qr-code`

**功能描述**: 生成包含当日唯一token的二维码数据，用于后续生成签到二维码。

**请求参数**: 无

**响应示例**:
```json
{
  "success": true,
  "message": "生成二维码成功",
  "data": {
    "qr_code_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "token": "a1b2c3d4e5f6g7h8",
    "date": "2024-01-15",
    "expires_at": "2024-01-15 23:59:59"
  }
}
```

**响应字段说明**:
- `qr_code_image`: Base64编码的二维码图片数据
- `token`: 当日唯一的签到token（16位）
- `date`: 生成日期（ISO格式）
- `expires_at`: 过期时间

**前端使用示例**:
```javascript
async function generateDailyQRCode() {
    try {
        const response = await fetch('/api/v1/attendance/qr-code');
        const result = await response.json();
        
        if (result.success) {
            // 直接显示二维码图片
            document.getElementById('qrImage').src = result.data.qr_code_image;
            
            // 显示有效期信息
            document.getElementById('expireTime').textContent = result.data.expires_at;
            
            // 保存token用于后续操作
            localStorage.setItem('dailyToken', result.data.token);
            localStorage.setItem('qrDate', result.data.date);
        }
    } catch (error) {
        console.error('生成二维码失败:', error);
    }
}
```

### 2. 生成URL二维码

**接口地址**: `POST /api/v1/attendance/qr-code-url`

**功能描述**: 根据提供的URL生成二维码图片，通常用于生成指向签到页面的二维码。

**请求参数**:
```json
{
  "url": "http://localhost:5000/checkin?token=a1b2c3d4e5f6g7h8&date=2024-01-15",
  "token": "a1b2c3d4e5f6g7h8",
  "date": "2024-01-15"
}
```

**参数说明**:
- `url` (必填): 要生成二维码的完整URL
- `token` (必填): 当日有效的签到token
- `date` (必填): 当前日期（YYYY-MM-DD格式）

**响应示例**:
```json
{
  "success": true,
  "message": "生成URL二维码成功",
  "data": {
    "qr_code_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "url": "http://localhost:5000/checkin?token=a1b2c3d4e5f6g7h8&date=2024-01-15",
    "token": "a1b2c3d4e5f6g7h8",
    "date": "2024-01-15"
  }
}
```

**前端使用示例**:
```javascript
async function generateCheckinQRCode() {
    try {
        // 首先获取当日token
        const tokenResponse = await fetch('/api/v1/attendance/qr-code');
        const tokenResult = await tokenResponse.json();
        
        if (tokenResult.success) {
            const token = tokenResult.data.token;
            const date = tokenResult.data.date;
            
            // 构建签到页面URL
            const checkinUrl = `${window.location.origin}/checkin?token=${token}&date=${date}`;
            
            // 生成包含URL的二维码
            const qrResponse = await fetch('/api/v1/attendance/qr-code-url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: checkinUrl,
                    token: token,
                    date: date
                })
            });
            
            const qrResult = await qrResponse.json();
            
            if (qrResult.success) {
                // 显示二维码
                document.getElementById('qrImage').src = qrResult.data.qr_code_image;
                document.getElementById('qrUrl').textContent = qrResult.data.url;
            }
        }
    } catch (error) {
        console.error('生成签到二维码失败:', error);
    }
}
```

### 3. 二维码签到

**接口地址**: `POST /api/v1/attendance/qr-checkin`

**功能描述**: 通过扫描二维码进行签到，无需JWT认证。

**请求参数**:
```json
{
  "token": "a1b2c3d4e5f6g7h8",
  "user_name": "张三",
  "emotion_status": "开心"
}
```

**参数说明**:
- `token` (必填): 从二维码中获取的签到token
- `user_name` (必填): 用户姓名（必须与数据库中的full_name字段完全匹配）
- `emotion_status` (可选): 心情状态

**响应示例**:
```json
{
  "success": true,
  "message": "张三 签到成功",
  "code": 201,
  "data": {
    "user_name": "张三",
    "check_in_time": "2024-01-15T08:30:00",
    "method": "扫码"
  }
}
```

**错误响应示例**:
```json
{
  "success": false,
  "message": "二维码已过期或无效",
  "code": 400
}
```

## 前端集成示例

### 完整的二维码生成和显示组件

```html
<!DOCTYPE html>
<html>
<head>
    <title>签到二维码</title>
    <style>
        .qr-container {
            text-align: center;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            max-width: 400px;
            margin: 0 auto;
        }
        
        .qr-image {
            max-width: 250px;
            height: auto;
            border: 1px solid #eee;
            border-radius: 5px;
        }
        
        .qr-info {
            margin-top: 15px;
            color: #666;
            font-size: 14px;
        }
        
        .refresh-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        
        .refresh-btn:hover {
            background: #0056b3;
        }
        
        .loading {
            color: #999;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="qr-container">
        <h2>扫码签到</h2>
        <div id="qrDisplay">
            <div class="loading">正在生成二维码...</div>
        </div>
        <div class="qr-info">
            <div id="qrInfo"></div>
        </div>
        <button class="refresh-btn" onclick="refreshQRCode()">刷新二维码</button>
    </div>

    <script>
        // 页面加载时生成二维码
        document.addEventListener('DOMContentLoaded', function() {
            generateQRCode();
        });

        async function generateQRCode() {
            const qrDisplay = document.getElementById('qrDisplay');
            const qrInfo = document.getElementById('qrInfo');
            
            // 显示加载状态
            qrDisplay.innerHTML = '<div class="loading">正在生成二维码...</div>';
            qrInfo.innerHTML = '';
            
            try {
                // 1. 获取当日token
                const tokenResponse = await fetch('/api/v1/attendance/qr-code');
                const tokenResult = await tokenResponse.json();
                
                if (!tokenResult.success) {
                    throw new Error(tokenResult.message);
                }
                
                const { token, date } = tokenResult.data;
                
                // 2. 构建签到页面URL
                const checkinUrl = `${window.location.origin}/checkin?token=${token}&date=${date}`;
                
                // 3. 生成包含URL的二维码
                const qrResponse = await fetch('/api/v1/attendance/qr-code-url', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        url: checkinUrl,
                        token: token,
                        date: date
                    })
                });
                
                const qrResult = await qrResponse.json();
                
                if (!qrResult.success) {
                    throw new Error(qrResult.message);
                }
                
                // 4. 显示二维码
                qrDisplay.innerHTML = `
                    <img src="${qrResult.data.qr_code_image}" 
                         alt="签到二维码" 
                         class="qr-image">
                `;
                
                // 5. 显示信息
                qrInfo.innerHTML = `
                    <strong>生成时间:</strong> ${date}<br>
                    <strong>有效期:</strong> 当日23:59<br>
                    <small>Token: ${token}</small>
                `;
                
            } catch (error) {
                qrDisplay.innerHTML = `
                    <div style="color: #dc3545; padding: 20px;">
                        生成失败<br>
                        <small>${error.message}</small>
                    </div>
                `;
                console.error('生成二维码失败:', error);
            }
        }
        
        function refreshQRCode() {
            generateQRCode();
        }
        
        // 每小时自动刷新
        setInterval(generateQRCode, 60 * 60 * 1000);
    </script>
</body>
</html>
```

### React 组件示例

```jsx
import React, { useState, useEffect } from 'react';

const QRCodeGenerator = () => {
    const [qrData, setQrData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const generateQRCode = async () => {
        setLoading(true);
        setError(null);
        
        try {
            // 获取token
            const tokenResponse = await fetch('/api/v1/attendance/qr-code');
            const tokenResult = await tokenResponse.json();
            
            if (!tokenResult.success) {
                throw new Error(tokenResult.message);
            }
            
            const { token, date } = tokenResult.data;
            const checkinUrl = `${window.location.origin}/checkin?token=${token}&date=${date}`;
            
            // 生成二维码
            const qrResponse = await fetch('/api/v1/attendance/qr-code-url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: checkinUrl,
                    token: token,
                    date: date
                })
            });
            
            const qrResult = await qrResponse.json();
            
            if (!qrResult.success) {
                throw new Error(qrResult.message);
            }
            
            setQrData({
                image: qrResult.data.qr_code_image,
                token: token,
                date: date,
                url: checkinUrl
            });
            
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        generateQRCode();
        
        // 每小时自动刷新
        const interval = setInterval(generateQRCode, 60 * 60 * 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="qr-generator">
            <h2>扫码签到</h2>
            
            {loading && <div>正在生成二维码...</div>}
            
            {error && (
                <div className="error">
                    生成失败: {error}
                    <button onClick={generateQRCode}>重试</button>
                </div>
            )}
            
            {qrData && (
                <div className="qr-display">
                    <img src={qrData.image} alt="签到二维码" />
                    <div className="qr-info">
                        <p>生成时间: {qrData.date}</p>
                        <p>有效期: 当日23:59</p>
                        <small>Token: {qrData.token}</small>
                    </div>
                </div>
            )}
            
            <button onClick={generateQRCode} disabled={loading}>
                刷新二维码
            </button>
        </div>
    );
};

export default QRCodeGenerator;
```

## 错误处理

### 常见错误码

| 错误码 | 错误信息 | 原因 | 解决方案 |
|--------|----------|------|----------|
| 400 | 缺少必要参数 | 请求参数不完整 | 检查请求参数是否完整 |
| 400 | 日期无效 | 提供的日期不是今天 | 使用当前日期 |
| 400 | token无效 | token已过期或错误 | 重新获取当日token |
| 400 | 二维码已过期或无效 | 签到时使用了过期token | 刷新二维码获取新token |
| 400 | 请填写姓名 | 签到时未提供姓名 | 确保提供用户姓名 |
| 400 | 今日已签到 | 用户今天已经签到过 | 提示用户已签到 |
| 404 | 用户不存在 | 姓名在数据库中不存在 | 检查姓名拼写是否正确 |
| 500 | 服务器内部错误 | 服务器异常 | 联系管理员或重试 |

### 错误处理示例

```javascript
async function handleQRCodeGeneration() {
    try {
        const response = await fetch('/api/v1/attendance/qr-code');
        const result = await response.json();
        
        if (!result.success) {
            // 根据错误码进行不同处理
            switch (response.status) {
                case 400:
                    showError('请求参数错误: ' + result.message);
                    break;
                case 500:
                    showError('服务器错误，请稍后重试');
                    break;
                default:
                    showError('未知错误: ' + result.message);
            }
            return;
        }
        
        // 成功处理
        displayQRCode(result.data);
        
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            showError('网络连接失败，请检查网络');
        } else {
            showError('请求失败: ' + error.message);
        }
    }
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // 3秒后自动隐藏
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 3000);
}
```

## 安全说明

### Token 生成机制

1. **算法**: 使用SHA256哈希算法
2. **输入**: 当前日期 + 固定密钥
3. **输出**: 取哈希值前16位作为token
4. **有效期**: 仅当日有效，次日自动失效

### 安全建议

1. **密钥管理**: 生产环境中应将密钥存储在环境变量或配置文件中
2. **HTTPS**: 生产环境必须使用HTTPS协议
3. **频率限制**: 建议对API接口添加频率限制
4. **日志记录**: 记录所有签到操作的日志
5. **输入验证**: 严格验证用户输入的姓名格式

### 配置建议

```python
# 生产环境配置示例
import os

class Config:
    # 从环境变量读取密钥
    ATTENDANCE_SECRET_KEY = os.environ.get('ATTENDANCE_SECRET_KEY', 'default_key')
    
    # 二维码配置
    QR_CODE_SIZE = 10
    QR_CODE_BORDER = 4
    QR_CODE_ERROR_CORRECTION = 'L'
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## 总结

本文档提供了完整的签到二维码生成API使用说明，包括：

1. **三个核心API接口**的详细说明
2. **前端集成示例**（原生JavaScript和React）
3. **完整的错误处理**机制
4. **安全性考虑**和最佳实践

开发人员可以根据这些说明在任何界面中集成二维码签到功能，确保系统的一致性和安全性。

如有疑问，请联系系统管理员或查看源代码中的详细实现。