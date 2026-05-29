#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取即开票产品数据和图片
"""
import os
import json
import requests
from urllib.parse import urljoin
from datetime import datetime

# 配置
BASE_URL = "https://www.lottery.gov.cn"
DATA_URL = "https://www.lottery.gov.cn/push/xdgg/dgg.pdata"
STATIC_BASE = "https://static.sporttery.cn/res_1_0/tcw/upload"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

# 创建目录
os.makedirs(IMAGE_DIR, exist_ok=True)


def download_image(url, filename):
    """下载图片"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            with open(os.path.join(IMAGE_DIR, filename), 'wb') as f:
                f.write(response.content)
            print(f"下载成功: {filename}")
            return True
        else:
            print(f"下载失败 {filename}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"下载错误 {filename}: {e}")
        return False


def main():
    """主函数"""
    print("开始获取即开票产品数据...")
    
    # 从之前浏览器中看到的产品信息，整理产品列表
    products = [
        {
            "id": 1,
            "name": "新春大吉2026",
            "price": "50元",
            "max_prize": "100万元",
            "desc": "马年新春大吉！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202601/08103053dzzn.jpg",
            "image_name": "01_新春大吉2026_50元.jpg"
        },
        {
            "id": 2,
            "name": "抢头彩2026",
            "price": "30元",
            "max_prize": "100万元",
            "desc": "马年新春抢头彩！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202601/08101001qqbz.jpg",
            "image_name": "02_抢头彩2026_30元.jpg"
        },
        {
            "id": 3,
            "name": "马到成功",
            "price": "20元",
            "max_prize": "100万元",
            "desc": "新的一年，马到成功！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202601/08095547tki3.jpg",
            "image_name": "03_马到成功_20元.jpg"
        },
        {
            "id": 4,
            "name": "骏马贺岁",
            "price": "10元",
            "max_prize": "30万元",
            "desc": "骏马贺新岁！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202601/08094832b2ki.jpg",
            "image_name": "04_骏马贺岁_10元.jpg"
        },
        {
            "id": 5,
            "name": "午马",
            "price": "5元",
            "max_prize": "10万元",
            "desc": "马年马力全开！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202601/08093148jdq0.jpg",
            "image_name": "05_午马_5元.jpg"
        },
        {
            "id": 6,
            "name": "激情全运",
            "price": "20元",
            "max_prize": "100万元",
            "desc": "助力体育赛事，喜迎十五运会！",
            "image_url": "https://static.sporttery.cn/res_1_0/jcw/upload/202508/29145436mw3u.jpg",
            "image_name": "06_激情全运_20元.jpg"
        },
        {
            "id": 7,
            "name": "八段锦",
            "price": "10元",
            "max_prize": "8万元",
            "desc": "古法健身，八段锦！",
            "image_url": "https://static.sporttery.cn/res_1_0/jcw/upload/202508/29144847dggz.jpg",
            "image_name": "07_八段锦_10元.jpg"
        },
        {
            "id": 8,
            "name": "体育科普 即刻出彩II",
            "price": "10元",
            "max_prize": "25万元",
            "desc": "体育知识，看我科普！",
            "image_url": "https://static.sporttery.cn/res_1_0/jcw/upload/202508/29143423hn8g.jpg",
            "image_name": "08_体育科普_10元.jpg"
        },
        {
            "id": 9,
            "name": "说走就走III",
            "price": "10元",
            "max_prize": "25万元",
            "desc": "自在随心，说走就走！",
            "image_url": "https://static.sporttery.cn/res_1_0/jcw/upload/202508/29142822ybsb.jpg",
            "image_name": "09_说走就走III_10元.jpg"
        },
        {
            "id": 10,
            "name": "珍稀宝贝",
            "price": "10元",
            "max_prize": "25万元",
            "desc": "别让珍贵变稀有！",
            "image_url": "https://static.sporttery.cn/res_1_0/jcw/upload/202508/29141245h6bg.jpg",
            "image_name": "10_珍稀宝贝_10元.jpg"
        },
        {
            "id": 11,
            "name": "好运全开",
            "price": "10元",
            "max_prize": "10万元",
            "desc": "好运全开",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202507/02143144y407.jpg",
            "image_name": "11_好运全开_10元.jpg"
        },
        {
            "id": 12,
            "name": "嘶嘶大闯关",
            "price": "20元",
            "max_prize": "100万元",
            "desc": "嘶嘶大闯关，快乐顶呱刮！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202507/02142430x3mk.jpg",
            "image_name": "12_嘶嘶大闯关_20元.jpg"
        },
        {
            "id": 13,
            "name": "麒麟王",
            "price": "20元",
            "max_prize": "100万元",
            "desc": "麒麟献祥瑞！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202504/290929015abx.jpg",
            "image_name": "13_麒麟王_20元.jpg"
        },
        {
            "id": 14,
            "name": "行大运（50元）",
            "price": "50元",
            "max_prize": "100万元",
            "desc": "发现惊喜，一起行大运！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202504/01095724ax4p.jpg",
            "image_name": "14_行大运_50元.jpg"
        },
        {
            "id": 15,
            "name": "行大运（30元）",
            "price": "30元",
            "max_prize": "100万元",
            "desc": "发现惊喜，一起行大运！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202504/01104816cn26.jpg",
            "image_name": "15_行大运_30元.jpg"
        },
        {
            "id": 16,
            "name": "行大运（20元）",
            "price": "20元",
            "max_prize": "100万元",
            "desc": "发现惊喜，一起行大运！",
            "image_url": "https://static.sporttery.cn/res_1_0/tcw/upload/202504/01110220liq4.jpg",
            "image_name": "16_行大运_20元.jpg"
        }
    ]
    
    # 保存产品数据到JSON
    data_output = {
        "title": "顶呱刮即开票产品素材",
        "source": "中国体彩网",
        "fetch_date": datetime.now().strftime("%Y-%m-%d"),
        "products": products
    }
    
    json_path = os.path.join(OUTPUT_DIR, "products.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data_output, f, ensure_ascii=False, indent=2)
    print(f"产品数据已保存到: {json_path}")
    
    # 下载图片
    print("\n开始下载产品图片...")
    for product in products:
        if product.get("image_url") and product.get("image_name"):
            download_image(product["image_url"], product["image_name"])
    
    # 生成产品介绍文档
    doc_content = """# 顶呱刮即开票产品素材

本素材来自中国体彩网，用于新场景售彩原型系统展示。

## 产品列表

"""
    for product in products:
        doc_content += f"""### {product['id']}. {product['name']}
- **面值**: {product['price']}
- **最高奖金**: {product['max_prize']}
- **产品介绍**: {product['desc']}

"""
    
    doc_path = os.path.join(OUTPUT_DIR, "products.md")
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc_content)
    print(f"\n产品介绍文档已保存到: {doc_path}")
    
    print("\n完成!")


if __name__ == "__main__":
    main()
