import requests
import time
import os
import random
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# save response content to this directory
output_dir = 'gptsapp_io\\output'
output_links = 'gptsapp_io\\output\\links0.txt'

def send_request(url, headers):
    retries = 3  # 设置重试次数
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                time.sleep(random.randint(1, 3))
                return response.content
            else:
                print(f"Request failed with status code: {response.status_code}")
                time.sleep(random.randint(1, 3))
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(random.randint(1, 3))
    return None

def process_page(page, headers):
    url = f"https://gptsapp.io/store?page={page}"
    response_content = send_request(url, headers)

    if response_content:
        soup = BeautifulSoup(response_content, 'html.parser')
        links = soup.select('h6.fw-semibold.mb-1.line-clamp-1 > a')
        if not links:
            print("No more links found on this page.")
            return True  # 返回True表示找不到链接
        for link in links:
            href = link.get('href')
            product_url = f"{href}"
            save_to_file(product_url, output_links)
    else:
        print(f"Failed to retrieve page {page}")
        return False  # 返回False表示请求失败

    return False  # 如果找到了链接,返回False继续下一页

def save_to_file(data, output_file):
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(data + '\n')

def batch_process(headers):
    os.makedirs(output_dir, exist_ok=True)
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = []
        page = 1019
        while True:
            print(f"Processing page {page}...")
            future = executor.submit(process_page, page, headers)
            futures.append(future)
            page += 1
            for completed_future in as_completed(futures):
                if completed_future.result() is True:  # 如果process_page返回True,说明找不到链接了
                    print("Search completed.")
                    return
            time.sleep(3)
            
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cookie': 'token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkluZ3dNMHhyUVhkb2JuVlZWR1YwWmtWa2J6VkthR2N4TnpFd09UQTFORFkzT0RNd0lnPT0iLCJleHAiOm51bGwsInB1ciI6ImNvb2tpZS50b2tlbiJ9fQ%3D%3D--ffcda3e30be89bfc552ae4b79bc51a0ad0dc4aa4; guest_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkluZ3dNMHhyUVhkb2JuVlZWR1YwWmtWa2J6VkthR2N4TnpFd09UQTFORFkzT0RNd0lnPT0iLCJleHAiOm51bGwsInB1ciI6ImNvb2tpZS5ndWVzdF90b2tlbiJ9fQ%3D%3D--b5913e6f444bf5dd19fdf0fd886dcd2aeb1346be; _ga=GA1.1.673055528.1710905604; _clck=190073k%7C2%7Cfk9%7C0%7C1540; cf_clearance=xpBD9eXAjuxF5UqxsHIYGUm91OOZa185_KrAtxMykgY-1710986278-1.0.1.1-.fUJrB_Ffhg3Gmmj17mKgLM9DxXUK_Fc70eJQWuNeeaUPbkdYr4QdGxYkNcDH2K5fWZSWgM_LmXdw0o3vseWMg; _clsk=qiwio9%7C1710986373658%7C20%7C1%7Ch.clarity.ms%2Fcollect; _app_session=jsqxBB1XSZNRICZRV26g2uTbSvUEIP65oN6H%2F%2FOTCRWtilxZ3ZemP35NOAFo2A8w3BV2lHkSt1v3d6xHE3FU4nv1GSI8lcBhsyKIqMFWzeJk7BbqW9Hecua5ypEhJbUsdxsyOQRFkVgPj97i752Ub1V28elLyXD2bH6M4VQCcgTAjnHG1Og%2FZwx%2B%2FHLeXGvh9GfSukqJ4eF8cfOOzMCtKetYdP4eyJ79JSoJYpP%2Bdho3Cfw1sxQjwVdPeUmGTpTcpGWASdSGQ9koM7XunQ0RAnuUD4yvKRxc1IwvFtn3iQFaNsMzvXbKsa%2BIuORW3HDMsxSPPXohHlpdvE0AXp9xCaVTL6cJUqdAT1qoR4SCSBfcp0htuiaUTA%3D%3D--UiKQYpKLMXuHMPMX--k4V%2BK3Vg1tDQyqJbz9nQNQ%3D%3D; _ga_W00BYFSXLJ=GS1.1.1710985296.4.1.1710986472.0.0.0',
    'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}


batch_process(headers)