#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新下载即开票产品图片 - 使用session保持cookie
"""
import os
import json
import requests
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# 创建session
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
})

# 先访问主页获取cookie
print("1. 访问主页获取session...")
try:
    resp = session.get("https://www.lottery.gov.cn/", timeout=15)
    print(f"   主页状态: {resp.status_code}")
except Exception as e:
    print(f"   主页错误: {e}")

# 访问产品列表页
print("\n2. 访问产品列表页...")
try:
    resp = session.get("https://www.lottery.gov.cn/xdgg/cpdq/?p=1", timeout=15)
    print(f"   列表页状态: {resp.status_code}, 长度: {len(resp.text)}")
except Exception as e:
    print(f"   列表页错误: {e}")

# 尝试不同的图片URL模式
# 从网络请求中看到的真实图片URL
image_candidates = [
    # 模式1: 直接CDN路径
    {
        "name": "新春大吉2026_50元.jpg",
        "urls": [
            "https://static.sporttery.cn/res_1_0/tcw/upload/202601/08103053dzzn.jpg",
            "https://static.sporttery.cn/res_1_0/tcw/images/dgg/202601/08103053dzzn.jpg",
        ]
    },
    {
        "name": "抢头彩2026_30元.jpg",
        "urls": [
            "https://static.sporttery.cn/res_1_0/tcw/upload/202601/08101001qqbz.jpg",
            "https://static.sporttery.cn/res_1_0/tcw/images/dgg/202601/08101001qqbz.jpg",
        ]
    },
]

# 测试哪个URL能返回真实图片
print("\n3. 测试图片URL...")
for item in image_candidates:
    for url in item["urls"]:
        try:
            r = session.get(url, timeout=15)
            ct = r.headers.get('content-type', '')
            size = len(r.content)
            is_image = size > 5000 and ('image' in ct or r.content[:2] == b'\xff\xd8')
            print(f"   {item['name']}: {url}")
            print(f"      -> status={r.status_code} type={ct} size={size} image={'YES' if is_image else 'NO'}")
            if is_image:
                print(f"      *** 找到有效图片URL! ***")
                break
        except Exception as e:
            print(f"   Error: {e}")

# 方案B: 从产品详情页提取图片
print("\n4. 尝试从产品详情页获取...")
detail_urls = [
    "https://www.lottery.gov.cn/xdgg/cpdxx/index.html?id=xchd2026",
]
for url in detail_urls:
    try:
        r = session.get(url, timeout=15)
        if 'image' in r.headers.get('content-type', '') or '<img' in r.text:
            print(f"   详情页有内容: {len(r.text)} bytes")
            # 提取img src
            import re
            imgs = re.findall(r'src=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']', r.text, re.I)
            for img in imgs[:5]:
                full_url = img if img.startswith('http') else f"https://www.lottery.gov.cn{img}"
                print(f"   找到图片: {full_url}")
    except Exception as e:
        print(f"   详情页错误: {e}")

# 方案C: 使用体彩官方API
print("\n5. 尝试体彩官方API...")
api_url = "https://www.lottery.gov.cn/push/xdgg/dgg.pdata"
try:
    r = session.get(api_url, timeout=15)
    print(f"   API状态: {r.status_code}, 类型: {r.headers.get('content-type')}")
    data = r.json() if 'json' in r.headers.get('content-type', '') else None
    if data:
        print(f"   API返回数据!")
        with open(os.path.join(OUTPUT_DIR, "api_data.json"), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"   API错误: {e}")

print("\n完成测试!")
