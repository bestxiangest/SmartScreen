#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Flask路由注册
"""

import requests

def test_routes():
    """测试各种路由"""
    base_url = 'http://127.0.0.1:5000'
    
    routes_to_test = [
        '/health',
        '/api/test',
        '/api/v1/auth/login',
        '/api/v1/roles',
        '/api/v1/users'
    ]
    
    for route in routes_to_test:
        try:
            response = requests.get(f"{base_url}{route}")
            print(f"路由 {route}: 状态码 {response.status_code}")
            if response.status_code == 404:
                print(f"  -> 404 Not Found")
            elif response.status_code == 401:
                print(f"  -> 401 Unauthorized (需要认证)")
            elif response.status_code == 200:
                print(f"  -> 200 OK")
            else:
                print(f"  -> 其他状态码: {response.status_code}")
        except Exception as e:
            print(f"路由 {route}: 请求失败 - {e}")
        print()

if __name__ == '__main__':
    print("测试Flask路由注册...")
    test_routes()