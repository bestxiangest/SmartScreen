#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

def test_fixed_routes():
    """测试修复后的API路由"""
    base_url = "http://127.0.0.1:5000"
    
    # 测试修复后的路由
    routes_to_test = [
        '/api/v1/announcements',
        '/api/v1/projects', 
        '/api/v1/schedules',
        '/api/v1/labs',
        '/api/v1/devices'
    ]
    
    print("测试修复后的API路由...")
    print("=" * 50)
    
    for route in routes_to_test:
        try:
            response = requests.get(f"{base_url}{route}")
            print(f"路由 {route}: 状态码 {response.status_code}")
            
            # 如果是401，说明路由存在但需要认证
            if response.status_code == 401:
                print(f"  -> 401 Unauthorized (需要认证) - 路由正常")
            # 如果是200，说明路由正常工作
            elif response.status_code == 200:
                print(f"  -> 200 OK - 路由正常工作")
            # 如果是404，说明路由不存在
            elif response.status_code == 404:
                print(f"  -> 404 Not Found - 路由不存在")
            else:
                print(f"  -> 其他状态码: {response.status_code}")
                
        except Exception as e:
            print(f"路由 {route}: 请求失败 - {str(e)}")
    
    print("=" * 50)
    print("测试完成")

if __name__ == "__main__":
    test_fixed_routes()