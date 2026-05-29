#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载即开票产品图片 - AI生成版本
"""
import os
import requests
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(SCRIPT_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

with open(os.path.join(SCRIPT_DIR, "products.json"), 'r', encoding='utf-8') as f:
    data = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0"
}

print(f"开始下载 {len(data['products'])} 张产品图片...")

for i, product in enumerate(data["products"]):
    url = product["image_url"]
    filename = product["image_name"]
    filepath = os.path.join(IMAGE_DIR, filename)
    
    print(f"[{i+1}/{len(data['products'])}] 下载: {filename}")
    try:
        r = requests.get(url, headers=headers, timeout=60)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            print(f"   成功: {len(r.content)} bytes")
        else:
            print(f"   失败: status={r.status_code}, size={len(r.content)}")
    except Exception as e:
        print(f"   错误: {e}")

print("\n完成!")
