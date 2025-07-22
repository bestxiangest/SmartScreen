#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import date
import hashlib

# 生成今日有效token
today = date.today().isoformat()
secret_key = "smartscreen_attendance_2024"
token_data = f"{today}_{secret_key}"
valid_token = hashlib.sha256(token_data.encode()).hexdigest()[:16]

print(f"今日日期: {today}")
print(f"有效token: {valid_token}")

# 测试API调用
url = "http://127.0.0.1:5000/api/v1/attendance/qr-checkin"
data = {
    "token": valid_token,
    "user_name": "陈都",
    "emotion_status": "开心"
}

print(f"\n发送的数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

try:
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    print(f"\n响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.headers.get('content-type', '').startswith('application/json'):
        result = response.json()
        print(f"\n解析后的响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"请求失败: {e}")