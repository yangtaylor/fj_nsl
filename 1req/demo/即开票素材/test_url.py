#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试图片URL是否有效"""
import requests
import os

# 测试URL列表
test_urls = [
    ("新春大吉2026", "https://static.sporttery.cn/res_1_0/tcw/upload/202601/08103053dzzn.jpg"),
    ("抢头彩2026", "https://static.sporttery.cn/res_1_0/tcw/upload/202601/08101001qqbz.jpg"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.lottery.gov.cn/",
}

for name, url in test_urls:
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=15)
        print(f"\n=== {name} ===")
        print(f"  URL: {url}")
        print(f"  Status: {r.status_code}")
        print(f"  Content-Type: {r.headers.get('content-type')}")
        print(f"  Size: {len(r.content)} bytes")
        print(f"  Final URL: {r.url}")
        # 检查前100字节是否像图片
        if len(r.content) > 4:
            header = r.content[:4]
            print(f"  File header (hex): {header.hex()}")
            # JPEG magic bytes: FF D8 FF
            if header[:2] == b'\xff\xd8':
                print("  -> Valid JPEG!")
            elif header[:3] == b'\x89PNG':
                print("  -> Valid PNG!")
            else:
                print(f"  -> NOT an image! First bytes: {r.content[:100]}")
    except Exception as e:
        print(f"Error {name}: {e}")
