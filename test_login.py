#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录并获取访问令牌
"""

import requests
import json

def test_login():
    """测试登录功能"""
    url = 'http://127.0.0.1:5000/api/v1/auth/login'
    
    # 测试登录数据
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(url, json=login_data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                token = data['data']['token']
                print(f"\n登录成功！")
                print(f"访问令牌: {token}")
                return token
            else:
                print(f"登录失败: {data.get('message')}")
        else:
            print(f"HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"请求失败: {e}")
    
    return None

def test_roles_api(token):
    """测试角色API"""
    url = 'http://127.0.0.1:5000/api/v1/roles'
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\n角色API状态码: {response.status_code}")
        print(f"角色API响应: {response.text}")
        
    except Exception as e:
        print(f"角色API请求失败: {e}")

if __name__ == '__main__':
    print("测试登录和角色API...")
    token = test_login()
    
    if token:
        test_roles_api(token)
    else:
        print("无法获取访问令牌，跳过角色API测试")