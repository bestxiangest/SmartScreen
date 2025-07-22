# 服务器JWT错误修复指南

## 问题描述
服务器上出现 `500 Internal Server Error` 和 `Missing required parameter 'digestmod'` 错误，这是由于Flask-JWT-Extended在某些Python环境下的HMAC兼容性问题导致的。

## 错误原因
1. **HMAC digestmod参数缺失**: 在较新版本的Python中，`hmac.new()` 函数要求显式指定 `digestmod` 参数
2. **JWT算法配置缺失**: Flask-JWT-Extended在某些环境下需要显式指定JWT算法
3. **环境差异**: Windows本地环境和Linux服务器环境的Python/包版本差异

## 修复步骤

### 1. 更新配置文件
确保 `config.py` 中包含JWT算法配置：
```python
# JWT配置
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string-smartscreen')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_ALGORITHM = 'HS256'  # 显式指定JWT算法，解决digestmod问题
```

### 2. 应用HMAC补丁
在 `app/__init__.py` 中已添加HMAC修复补丁：
```python
# 修复JWT HMAC digestmod问题
def patch_jwt_hmac():
    """修复Flask-JWT-Extended在某些环境下的HMAC digestmod问题"""
    try:
        import hmac
        import hashlib
        
        # 保存原始的hmac.new函数
        original_hmac_new = hmac.new
        
        def patched_hmac_new(key, msg=None, digestmod=None):
            """确保HMAC调用时总是包含digestmod参数"""
            if digestmod is None:
                digestmod = hashlib.sha256
            return original_hmac_new(key, msg, digestmod)
        
        # 替换hmac.new函数
        hmac.new = patched_hmac_new
        
    except Exception:
        # 如果补丁失败，静默忽略，让应用继续运行
        pass

# 在导入JWT相关模块之前应用补丁
patch_jwt_hmac()
```

### 3. 服务器部署步骤

#### 3.1 上传修复后的文件
将以下修复后的文件上传到服务器：
- `config.py`
- `app/__init__.py`
- `app/models.py` (已更新为scrypt密码哈希)
- `app/api/users.py` (已更新为scrypt密码哈希)
- `create_admin.py` (已更新为scrypt密码哈希)

#### 3.2 重启服务器应用
```bash
# 停止当前运行的应用
sudo systemctl stop your-app-service
# 或者使用 pkill 停止进程
pkill -f "python.*app.py"

# 重新启动应用
sudo systemctl start your-app-service
# 或者直接运行
cd /www/wwwroot/SmartScreen
python app.py
```

#### 3.3 检查服务器环境
如果问题仍然存在，检查服务器环境：
```bash
# 检查Python版本
python --version

# 检查关键包版本
pip show Flask-JWT-Extended
pip show PyJWT
pip show Werkzeug

# 运行诊断脚本
python debug_jwt.py
```

### 4. 验证修复效果

#### 4.1 测试登录API
```bash
curl -X POST http://xs.sharpcaterpillar.top:5555/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### 4.2 检查服务器日志
```bash
# 查看应用日志
tail -f /var/log/your-app.log

# 或者查看系统日志
journalctl -u your-app-service -f
```

### 5. 备用解决方案

如果上述修复仍不生效，可以尝试：

#### 5.1 更新依赖包
```bash
pip install --upgrade Flask-JWT-Extended PyJWT
```

#### 5.2 使用固定版本
在 `requirements.txt` 中指定兼容版本：
```
Flask-JWT-Extended==4.5.3
PyJWT==2.8.0
```

#### 5.3 环境变量配置
设置环境变量强制指定JWT算法：
```bash
export JWT_ALGORITHM=HS256
```

## 技术说明

### 问题根源
- Python 3.8+ 中，`hmac.new()` 函数的 `digestmod` 参数变为必需
- Flask-JWT-Extended 在某些版本中没有正确处理这个变化
- 不同操作系统的Python实现可能有细微差异

### 修复原理
1. **HMAC补丁**: 拦截 `hmac.new()` 调用，自动添加默认的 `digestmod` 参数
2. **算法显式指定**: 在JWT配置中明确指定使用 HS256 算法
3. **兼容性处理**: 确保在各种Python环境下都能正常工作

## 测试确认

本地测试结果显示修复成功：
- ✅ JWT令牌创建正常
- ✅ 用户登录功能正常
- ✅ API调用正常
- ✅ 密码验证正常

## 联系支持

如果在服务器部署过程中遇到问题，请提供：
1. 服务器错误日志
2. Python版本信息
3. 依赖包版本信息
4. `debug_jwt.py` 运行结果