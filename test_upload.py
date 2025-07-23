#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图片上传功能
"""

import requests
import json
import os
from io import BytesIO
from PIL import Image

# API基础URL
API_BASE_URL = "http://127.0.0.1:5000/api"

def create_test_image():
    """创建一个测试图片"""
    # 创建一个简单的测试图片
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def login():
    """登录获取token"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
    print(f"登录响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            token = data['data']['token']
            print(f"登录成功，获取到token: {token[:20]}...")
            return token
        else:
            print(f"登录失败: {data.get('message')}")
    else:
        print(f"登录请求失败: {response.text}")
    
    return None

def test_upload(token):
    """测试图片上传"""
    print("\n开始测试图片上传...")
    
    # 创建测试图片
    test_image = create_test_image()
    
    # 准备上传数据
    files = {
        'file': ('test_image.png', test_image, 'image/png')
    }
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # 发送上传请求
    response = requests.post(f"{API_BASE_URL}/upload/image", files=files, headers=headers)
    
    print(f"上传响应状态码: {response.status_code}")
    print(f"上传响应内容: {response.text}")
    
    if response.status_code == 201:
        data = response.json()
        if data.get('success'):
            print("✅ 图片上传成功!")
            print(f"文件URL: {data['data']['file_url']}")
            print(f"文件名: {data['data']['filename']}")
            print(f"文件大小: {data['data']['file_size']} bytes")
            return True
        else:
            print(f"❌ 上传失败: {data.get('message')}")
    else:
        print(f"❌ 上传请求失败: {response.text}")
    
    return False

def main():
    print("=== 图片上传功能测试 ===")
    
    # 1. 登录获取token
    token = login()
    if not token:
        print("❌ 无法获取登录token，测试终止")
        return
    
    # 2. 测试图片上传
    success = test_upload(token)
    
    if success:
        print("\n🎉 图片上传功能测试通过!")
    else:
        print("\n❌ 图片上传功能测试失败!")

if __name__ == "__main__":
    main()