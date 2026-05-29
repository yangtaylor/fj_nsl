#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用PIL绘制即开票模拟票面图片 - 用于原型系统展示
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont
import math

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# 产品数据
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

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill, outline=outline)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill, outline=outline)
    draw.pieslice([x1, y1, x1+2*radius, y1+2*radius], 180, 270, fill=fill, outline=outline)
    draw.pieslice([x2-2*radius, y1, x2, y1+2*radius], 270, 360, fill=fill, outline=outline)
    draw.pieslice([x1, y2-2*radius, x1+2*radius, y2], 90, 180, fill=fill, outline=outline)
    draw.pieslice([x2-2*radius, y2-2*radius, x2, y2], 0, 90, fill=fill, outline=outline)

def create_ticket_image(product, width=600, height=400):
    """创建模拟票面图片"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    color_rgb = hex_to_rgb(product['color'])

    # 背景
    draw.rectangle([0, 0, width, height], fill='#F8F8F8')

    # 顶部装饰条
    draw.rectangle([0, 0, width, 40], fill=color_rgb)

    # 体彩logo区域
    draw.ellipse([20, 5, 55, 35], fill='white', outline=color_rgb, width=2)
    try:
        font_large = ImageFont.truetype("msyh.ttc", 16) if os.path.exists("C:/Windows/Fonts/msyh.ttc") else ImageFont.load_default()
        font_medium = ImageFont.truetype("msyh.ttc", 14) if os.path.exists("C:/Windows/Fonts/msyh.ttc") else ImageFont.load_default()
        font_small = ImageFont.truetype("msyh.ttc", 11) if os.path.exists("C:/Windows/Fonts/msyh.ttc") else ImageFont.load_default()
        font_big = ImageFont.truetype("msyhbd.ttc", 28) if os.path.exists("C:/Windows/Fonts/msyhbd.ttc") else ImageFont.load_default()
        font_price = ImageFont.truetype("msyhbd.ttc", 36) if os.path.exists("C:/Windows/Fonts/msyhbd.ttc") else ImageFont.load_default()
    except:
        font_large = font_medium = font_small = font_big = font_price = ImageFont.load_default()

    # 标题
    draw.text((width//2, 20), product['name'], fill='white', font=font_large, anchor='mm')

    # 主视觉区域 (中间大区域)
    visual_y = 70
    visual_h = 160
    # 渐变背景效果
    for i in range(visual_h):
        alpha = int(255 * (1 - i / visual_h * 0.3))
        r = min(255, color_rgb[0] + (248 - color_rgb[0]) * i // visual_h)
        g = min(255, color_rgb[1] + (248 - color_rgb[1]) * i // visual_h)
        b = min(255, color_rgb[2] + (248 - color_rgb[2]) * i // visual_h)
        draw.line([(30, visual_y + i), (width - 30, visual_y + i)], fill=(r, g, b))

    # 装饰图案 - 圆形
    cx, cy = width // 2, visual_y + visual_h // 2
    for r in range(80, 10, -15):
        opacity = int(100 * (1 - r / 80))
        c = (
            min(255, color_rgb[0] + opacity),
            min(255, color_rgb[1] + opacity),
            min(255, color_rgb[2] + opacity),
        )
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c, width=2)

    # 产品名称
    draw.text((cx, cy - 25), product['name'], fill='white', font=font_big, anchor='mm')

    # 面值区域
    price_y = 245
    draw_rounded_rect(draw, [width//2 - 80, price_y, width//2 + 80, price_y + 65], 10,
                     fill=color_rgb, outline=None)

    draw.text((width//2, price_y + 12), f"面值 {product['price']} 元", fill='white', font=font_medium, anchor='mm')

    # 最高奖金
    prize_text = f"最高奖金 {product['max_prize']//10000}万元"
    draw.text((width//2, price_y + 38), prize_text, fill='#FFD700', font=font_medium, anchor='mm')

    # 底部信息
    bottom_y = 330
    draw.line([(30, bottom_y), (width-30, bottom_y)], fill='#E0E0E0', width=1)

    # 描述文字
    draw.text((width//2, bottom_y + 18), product['desc'], fill='#666666', font=font_medium, anchor='mm')

    # 品牌标识
    draw.text((width - 20, height - 15), "体彩 | 顶呱刮", fill='#999999', font=font_small, anchor='rm')

    # 边框
    draw.rectangle([2, 2, width-3, height-3], outline=color_rgb, width=3)

    return img

print(f"开始生成 {len(products)} 张模拟票面图片...")
for i, product in enumerate(products):
    filename = f"{product['id']:02d}_{product['name']}_{product['price']}元.jpg"
    filepath = os.path.join(IMAGE_DIR, filename)
    
    print(f"[{i+1}/{len(products)}] 生成: {filename}")
    img = create_ticket_image(product)
    img.save(filepath, 'JPEG', quality=95)
    print(f"   已保存")

# 更新products.json中的image_url
for p in products:
    p["image_url"] = f"images/{p['id']:02d}_{p['name']}_{p['price']}元.jpg"
    p["image_name"] = f"{p['id']:02d}_{p['name']}_{p['price']}元.jpg"
    p["image_path"] = f"images/{p['id']:02d}_{p['name']}_{p['price']}元.jpg"

data_output = {
    "title": "顶呱刮即开票产品素材",
    "source": "原型系统展示用 (PIL绘制)",
    "note": "图片为程序绘制的模拟票面效果，正式交付需替换为官方授权素材",
    "fetch_date": __import__('datetime').datetime.now().strftime("%Y-%m-%d"),
    "products": products
}

json_path = os.path.join(OUTPUT_DIR, "products.json")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data_output, f, ensure_ascii=False, indent=2)

print(f"\n产品数据已更新: {json_path}")
print("\n完成! 所有图片已使用PIL重新生成")
