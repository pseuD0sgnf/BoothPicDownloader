import requests
from bs4 import BeautifulSoup
import os
import re
from google.colab import files

def download_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    # 提取商品标题
    h2_tag = soup.find('h2', {'class': 'font-bold leading-[32px] m-0 text-[24px]'})
    if h2_tag:
        product_title = h2_tag.text.strip()
    else:
        print("无法从页面中提取商品标题。")
        return
    forbidden_chars = r'[\/\?%\*\:\"\<\>\|]'
    product_title = re.sub(forbidden_chars, ' ', product_title)

    # 从URL中提取数字代码
    match = re.search(r'/(\d+)', url)
    if match:
        item_code = match.group(1)
    else:
        print("无法从URL中提取数字代码。")
        return

    # 寻找所有被指定<div>标签包裹的<img>标签
    images = soup.find_all('div', class_='slick-thumbnail-border')

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists('downloaded_images'):
        os.makedirs('downloaded_images')

    for i, div in enumerate(images):
        img = div.find('img')
        if img and 'src' in img.attrs:
            # 提取并处理图片URL
            img_url = re.sub(r'/c/\d+x\d+_a2_g5/', '/', img['src'])

            # 格式化文件名，后缀从01开始
            filename = f"[{item_code}] {product_title} {str(i+1).zfill(2)}.jpg"

            # 下载图片
            img_data = requests.get(img_url).content
            with open(os.path.join('downloaded_images', filename), 'wb') as file:
                file.write(img_data)
            print(f"Downloaded {filename}")

    return item_code

# Booth URL
url = "https://booth.pm/ja/items/5481291"

# 调用函数下载图片
item_code = download_images(url)

# 打包下载并删除
!zip -r {item_code}.zip downloaded_images
files.download(f"{item_code}.zip")
!rm -rf downloaded_images
print("已打包下载并删除。")
