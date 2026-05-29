#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Playwright浏览器访问中国体彩网，获取真实产品图片
"""
import os
import json
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# 产品详情页URL列表（从体彩网产品列表页获取）
# 格式: (产品名称, 面值, 详情页URL)
product_urls = [
    ("新春大吉2026", 50, "https://www.lottery.gov.cn/xdgg/cpxq/?id=211&c=1"),
    ("抢头彩2026", 30, "https://www.lottery.gov.cn/xdgg/cpxq/?id=210&c=1"),
    ("马到成功", 20, "https://www.lottery.gov.cn/xdgg/cpxq/?id=209&c=1"),
    ("骏马贺岁", 10, "https://www.lottery.gov.cn/xdgg/cpxq/?id=208&c=1"),
    ("午马", 5, "https://www.lottery.gov.cn/xdgg/cpxq/?id=207&c=1"),
    ("激情全运", 20, "https://www.lottery.gov.cn/xdgg/cpxq/?id=206&c=1"),
    ("八段锦", 10, "https://www.lottery.gov.cn/xdgg/cpxq/?id=205&c=1"),
    ("体育科普 即刻出彩II", 10, "https://www.lottery.gov.cn/xdgg/cpxq/?id=204&c=1"),
    ("说走就走III", 10, "https://www.lottery.gov.cn/xdgg/cpxq/?id=203&c=1"),
    ("珍稀宝贝", 10, "https://www.lottery.gov.cn/xdgg/cpxq/?id=202&c=1"),
    ("好运全开", 10, "https://www.lottery.gov.cn/xdgg/cpxq/?id=201&c=1"),
    ("嘶嘶大闯关", 20, "https://www.lottery.gov.cn/xdgg/cpxq/?id=200&c=1"),
    ("麒麟王", 20, "https://www.lottery.gov.cn/xdgg/cpxq/?id=199&c=1"),
    ("行大运（50元）", 50, "https://www.lottery.gov.cn/xdgg/cpxq/?id=198&c=1"),
    ("行大运（30元）", 30, "https://www.lottery.gov.cn/xdgg/cpxq/?id=197&c=1"),
    ("行大运（20元）", 20, "https://www.lottery.gov.cn/xdgg/cpxq/?id=196&c=1"),
]


async def download_product_images():
    """下载产品图片"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        # 先访问主页获取cookie
        print("访问主页...")
        await page.goto("https://www.lottery.gov.cn/", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        
        # 访问产品列表页
        print("访问产品列表页...")
        await page.goto("https://www.lottery.gov.cn/xdgg/cpdq/?p=1", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        
        products_data = []
        
        for idx, (name, price, detail_url) in enumerate(product_urls, 1):
            print(f"\n[{idx}/{len(product_urls)}] 处理: {name}")
            try:
                # 访问详情页
                await page.goto(detail_url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(2)
                
                # 获取页面内容
                content = await page.content()
                
                # 提取产品信息
                # 查找图片元素
                img_elements = await page.query_selector_all('img')
                image_urls = []
                for img in img_elements:
                    src = await img.get_attribute('src')
                    if src and ('upload' in src or 'jcw' in src or 'tcw' in src):
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = 'https://www.lottery.gov.cn' + src
                        image_urls.append(src)
                
                # 提取产品描述
                desc = ""
                # 尝试多种选择器获取描述
                desc_selectors = [
                    '.cp-detail-desc',
                    '.product-desc',
                    '.detail-content',
                    '[class*="desc"]',
                    '[class*="detail"]'
                ]
                for selector in desc_selectors:
                    try:
                        elem = await page.query_selector(selector)
                        if elem:
                            text = await elem.text_content()
                            if text and len(text.strip()) > 5:
                                desc = text.strip()[:200]
                                break
                    except:
                        pass
                
                # 提取最高奖金
                max_prize = 1000000  # 默认值
                page_text = await page.text_content('body')
                if '最高奖金' in page_text:
                    import re
                    match = re.search(r'最高奖金[：:]\s*(\d+)\s*万元', page_text)
                    if match:
                        max_prize = int(match.group(1)) * 10000
                
                # 下载主图片
                main_image_url = None
                for url in image_urls:
                    if url.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        main_image_url = url
                        break
                
                if main_image_url:
                    print(f"  找到图片: {main_image_url}")
                    # 下载图片
                    safe_name = name.replace('（', '(').replace('）', ')')
                    filename = f"{idx:02d}_{safe_name}_{price}元.jpg"
                    filepath = os.path.join(IMAGE_DIR, filename)
                    
                    try:
                        response = await page.evaluate(f"""
                            async () => {{
                                const resp = await fetch('{main_image_url}', {{
                                    headers: {{'Referer': 'https://www.lottery.gov.cn/'}}
                                }});
                                const blob = await resp.blob();
                                return await new Promise(resolve => {{
                                    const reader = new FileReader();
                                    reader.onloadend = () => resolve(reader.result);
                                    reader.readAsDataURL(blob);
                                }});
                            }}
                        """)
                        
                        if response and response.startswith('data:'):
                            import base64
                            data = response.split(',')[1]
                            img_data = base64.b64decode(data)
                            with open(filepath, 'wb') as f:
                                f.write(img_data)
                            print(f"  下载成功: {len(img_data)} bytes")
                        else:
                            print(f"  下载失败: 无法获取图片数据")
                    except Exception as e:
                        print(f"  下载错误: {e}")
                else:
                    print(f"  未找到图片")
                
                products_data.append({
                    "id": idx,
                    "name": name,
                    "price": price,
                    "max_prize": max_prize,
                    "desc": desc or f"{name}，面值{price}元",
                    "detail_url": detail_url,
                    "image_url": main_image_url,
                    "image_name": filename if main_image_url else None
                })
                
            except Exception as e:
                print(f"  处理错误: {e}")
                products_data.append({
                    "id": idx,
                    "name": name,
                    "price": price,
                    "max_prize": 1000000,
                    "desc": f"{name}，面值{price}元",
                    "detail_url": detail_url,
                    "image_url": None,
                    "image_name": None
                })
        
        await browser.close()
        
        # 保存数据
        data_output = {
            "title": "顶呱刮即开票产品素材",
            "source": "中国体彩网 (通过Playwright浏览器获取)",
            "note": "图片为从体彩官网获取的真实票面，用于原型系统展示",
            "fetch_date": __import__('datetime').datetime.now().strftime("%Y-%m-%d"),
            "products": products_data
        }
        
        with open(os.path.join(OUTPUT_DIR, "products_real.json"), 'w', encoding='utf-8') as f:
            json.dump(data_output, f, ensure_ascii=False, indent=2)
        
        print(f"\n完成! 已处理 {len(products_data)} 个产品")
        print(f"数据已保存到: products_real.json")


if __name__ == "__main__":
    asyncio.run(download_product_images())
