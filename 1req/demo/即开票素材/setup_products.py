#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成即开票模拟票面图片 - 用于原型系统展示
由于中国体彩网图片有反爬虫保护，使用AI生成模拟票面
"""
import os
import json
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# 产品列表 - 每个产品的详细信息
products = [
    {"id": 1, "name": "新春大吉2026", "price": 50, "max_prize": 1000000, "desc": "马年新春大吉！", "color": "#D42426", "theme": "马年春节"},
    {"id": 2, "name": "抢头彩2026", "price": 30, "max_prize": 1000000, "desc": "马年新春抢头彩！", "color": "#E67E22", "theme": "春节喜庆"},
    {"id": 3, "name": "马到成功", "price": 20, "max_prize": 1000000, "desc": "新的一年，马到成功！", "color": "#F39C12", "theme": "成功祝福"},
    {"id": 4, "name": "骏马贺岁", "price": 10, "max_prize": 300000, "desc": "骏马贺新岁！", "color": "#27AE60", "theme": "生肖贺岁"},
    {"id": 5, "name": "午马", "price": 5, "max_prize": 100000, "desc": "马年马力全开！", "color": "#2980B9", "theme": "生肖主题"},
    {"id": 6, "name": "激情全运", "price": 20, "max_prize": 1000000, "desc": "助力体育赛事，喜迎十五运会！", "color": "#8E44AD", "theme": "体育赛事"},
    {"id": 7, "name": "八段锦", "price": 10, "max_prize": 80000, "desc": "古法健身，八段锦！", "color": "#16A085", "theme": "传统养生"},
    {"id": 8, "name": "体育科普 即刻出彩II", "price": 10, "max_prize": 250000, "desc": "体育知识，看我科普！", "color": "#2C3E50", "theme": "科普教育"},
    {"id": 9, "name": "说走就走III", "price": 10, "max_prize": 250000, "desc": "自在随心，说走就走！", "color": "#D35400", "theme": "旅游出行"},
    {"id": 10, "name": "珍稀宝贝", "price": 10, "max_prize": 250000, "desc": "别让珍贵变稀有！", "color": "#7D3C98", "theme": "珍稀动物"},
    {"id": 11, "name": "好运全开", "price": 10, "max_prize": 100000, "desc": "好运全开", "color": "#C0392B", "theme": "好运祝福"},
    {"id": 12, "name": "嘶嘶大闯关", "price": 20, "max_prize": 1000000, "desc": "嘶嘶大闯关，快乐顶呱刮！", "color": "#1ABC9C", "theme": "游戏闯关"},
    {"id": 13, "name": "麒麟王", "price": 20, "max_prize": 1000000, "desc": "麒麟献祥瑞！", "color": "#E74C3C", "theme": "吉祥瑞兽"},
    {"id": 14, "name": "行大运（50元）", "price": 50, "max_prize": 1000000, "desc": "发现惊喜，一起行大运！", "color": "#3498DB", "theme": "好运财运"},
    {"id": 15, "name": "行大运（30元）", "price": 30, "max_prize": 1000000, "desc": "发现惊喜，一起行大运！", "color": "#9B59B6", "theme": "好运财运"},
    {"id": 16, "name": "行大运（20元）", "price": 20, "max_prize": 1000000, "desc": "发现惊喜，一起行大运！", "color": "#1ABC9C", "theme": "好运财运"},
]

# 图片URL列表 - 使用AI生成的占位图片
# 格式: https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={prompt}&image_size={size}
def generate_image_url(product):
    """生成AI图片URL"""
    prompt = f"""Chinese sports lottery scratch card ticket design for {product['name']}, face value {product['price']} yuan, max prize {product['max_prize']//10000}万元. 
{product['desc']}
Theme: {product['theme']}, main color: {product['color']}
Design elements: Chinese lottery style with gold foil effect, decorative border pattern, lottery logo area, scratch area simulation, prize ladder display, professional product packaging look, high quality commercial photography style"""
    
    encoded_prompt = prompt.replace(' ', '%20').replace(',', '%2C').replace(':', '%3A').replace('\n', '%0A')
    return f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=landscape_4_3"

# 保存产品数据
data_output = {
    "title": "顶呱刮即开票产品素材",
    "source": "中国体彩网 (原型系统展示用)",
    "note": "图片为AI生成模拟票面，正式交付需替换为官方授权素材",
    "fetch_date": datetime.now().strftime("%Y-%m-%d"),
    "products": [
        {
            **p,
            "image_url": generate_image_url(p),
            "image_name": f"{p['id']:02d}_{p['name']}_{p['price']}元.jpg",
            "image_path": f"images/{p['id']:02d}_{p['name']}_{p['price']}元.jpg"
        }
        for p in products
    ]
}

json_path = os.path.join(OUTPUT_DIR, "products.json")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data_output, f, ensure_ascii=False, indent=2)
print(f"产品数据已更新: {json_path}")

# 生成下载脚本
download_script = '''#!/usr/bin/env python3
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

print("\\n完成!")
'''

script_path = os.path.join(OUTPUT_DIR, "download_images.py")
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(download_script)
print(f"下载脚本已生成: {script_path}")

# 更新产品介绍文档
doc_content = """# 顶呱刮即开票产品素材

本素材用于新场景售彩原型系统展示。

> **注意:** 图片为AI生成的模拟票面效果，正式交付时需替换为中国体彩中心授权的官方素材。

## 产品列表

| 序号 | 名称 | 面值 | 最高奖金 | 主题 | 状态 |
|------|------|------|---------|------|------|
"""
for p in products:
    doc_content += f"| {p['id']} | {p['name']} | {p['price']}元 | {p['max_prize']//10000}万元 | {p['theme']} | 待下载 |\n"

doc_content += """
## 使用说明

1. 运行 `python download_images.py` 下载AI生成的模拟票面图片
2. 图片将保存在 `images/` 目录下
3. 正式交付前，需联系中国体彩中心获取官方授权素材并替换

## 文件结构

```
即开票素材/
├── images/           # 产品图片目录
│   ├── 01_新春大吉2026_50元.jpg
│   ├── 02_抢头彩2026_30元.jpg
│   └── ...
├── products.json     # 产品数据(JSON格式)
├── products.md       # 本文档
├── download_images.py # 图片下载脚本
└── fetch_products.py # 原始获取脚本
```
"""

doc_path = os.path.join(OUTPUT_DIR, "products.md")
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(doc_content)
print(f"产品文档已更新: {doc_path}")

print("\n配置完成! 请运行 download_images.py 下载图片")
