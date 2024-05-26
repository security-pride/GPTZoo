import json
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime
import os
import re
import humanfriendly
import random
import time
import argparse

# ssh xinyihou@222.20.126.132
# cd gpt_store/gptsapp_io
# python3 parse.py --file links_unique12.txt --start 9029

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def send_request(url, headers):
    retries = 3  # 设置重试次数
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                time.sleep(random.randint(1, 3))
                return response.content
            else:
                print(f"\nProcess exception: {url}--Request failed with status code: {response.status_code}")
                time.sleep(random.randint(1, 3))
                return None
        except requests.exceptions.RequestException as e:
            print(f"\nProcess exception: {url}--Request error: {e}")
            time.sleep(random.randint(1, 3))
    return None

def scrape_gpt_info(url, headers):
    html_content = send_request(url, headers)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')

        name_element = soup.find('h1', class_='h3 mb-0')
        if name_element:
            name = name_element.text.strip()
        else:
            name = 'Unknown'

        author_element = soup.find('b', {'data-author': True})
        if author_element:
            author = author_element.get('data-author')
        else:
            author = 'Unknown'

        rating_element = soup.find('div', {'data-rating': True})
        if rating_element:
            rating = rating_element.get('data-rating')
            rating_count = rating_element.get('data-rating-count')
            rating_max = rating_element.get('data-rating-max')
        else:
            rating = 'Unknown'
            rating_count = 'Unknown'
            rating_max = 'Unknown'

        review_count_element = soup.find('div', class_='rating-count')
        if review_count_element:
            review_count_text = review_count_element.get_text(strip=True)
            if review_count_text:
                # Remove non-digit characters from the string
                review_count_text = ''.join(char for char in review_count_text if char.isdigit())
                if review_count_text:
                    review_count = int(review_count_text)
                else:
                    review_count = 0
            else:
                review_count = 0
        else:
            review_count = 0

        chat_count_element = soup.find('span', {'aria-label': 'Chats'})
        if chat_count_element:
            chat_count_text = chat_count_element.text.strip()
            chat_count = humanfriendly.parse_size(chat_count_text)
        else:
            chat_count = 0

        features_element = soup.find('div', class_='text-muted d-flex flex-column flex-md-row mt-2')
        if features_element:
            features = [span.text.strip() for span in features_element.find_all('span')]
        else:
            features = []

        description_element = soup.find('div', class_='description my-3')
        if description_element:
            description = description_element.text.strip()
        else:
            description = ''

        tags_and_date_element = soup.find('div', class_='d-flex flex-column flex-md-row align-items-center justify-content-between')
        if tags_and_date_element:
            tags_element = tags_and_date_element.find('div', class_='tags d-flex flex-wrap align-items-center')
            tags = [a.text.strip() for a in tags_element.find_all('a', class_='badge bg-secondary me-2 mb-2')]
            date_element = tags_and_date_element.find('div', class_='fs-sm text-muted mb-2 flex-row-auto')
            release_date = date_element.text.strip()
        else:
            tags = []
            release_date = ''
        
        category_container = soup.find('strong', class_='text-nowrap me-2', string='Categories ')
        if category_container:
            category_element = category_container.find_next_sibling('span')
            if category_element:
                category = category_element.text.strip()
            else:
                category = ''
        else:
            category = ''

        update_info = {}
        update_date_elements = soup.find_all('li', class_='px-0 d-flex align-items-center list-group-item justify-content-between')
        for update_date_element in update_date_elements:
            datetime_span = update_date_element.find('span', {'datetime': True})
            if datetime_span:
                update_date_str = datetime_span.get('datetime')
            else:
                update_date_str = None

            update_name_element = update_date_element.find('strong', class_='text-nowrap me-2')
            if update_name_element:
                update_name = update_name_element.string
                if update_date_str:
                    update_info[update_name] = update_date_str

        share_recipient = {}
        share_recipient_section = soup.find('h3', class_='h5', string='Share recipient')
        if share_recipient_section:
            share_recipient_ul = share_recipient_section.find_next('ul', class_='list-group list-group-flush border-bottom mb-3')
            if share_recipient_ul:
                share_recipient_item = share_recipient_ul.find('li', class_='px-0 d-flex align-items-center list-group-item justify-content-between')
                if share_recipient_item:
                    recipient_name = share_recipient_item.find('strong').text.strip()
                    recipient_status = share_recipient_item.find('span', recursive=False).text.strip()
                    share_recipient[recipient_name] = recipient_status

        rating_div = soup.find('div', class_='fs-4 text-dark')
        if rating_div:
            official_rating_element = rating_div.find('b')
            if official_rating_element:
                official_rating = official_rating_element.text.strip()
            else:
                official_rating = 'N/A'
        else:
            official_rating = 'N/A'

        rating_count_div = soup.find('div', class_='fs-sm')
        if rating_count_div:
            rating_count_text = rating_count_div.text.strip()
            if 'Ratings' in rating_count_text:
                rating_count = rating_count_text.strip('Ratings ()').rstrip('+')
            else:
                rating_count = 'N/A'
        else:
            rating_count = 'N/A'

        conversation_starters = []
        conversation_starters_div = soup.find('div', class_='row row-cols-sm-2 row-cols-1 g-md-3 g-2')
        if conversation_starters_div:
            conversation_starter_cols = conversation_starters_div.find_all('div', class_='col')
            for col in conversation_starter_cols:
                content_div = col.find('div', class_='border bg-white text-truncate rounded-2 p-2')
                if content_div:
                    conversation_starters.append(content_div.text.strip())

        capabilities = []
        capabilities_div = soup.find('div', {'id': 'capabilities'})
        if capabilities_div:
            capabilities_table = capabilities_div.find('table')
            if capabilities_table:
                table_rows = capabilities_table.find('tbody').find_all('tr')
                for row in table_rows:
                    th_element = row.find('th')
                    if th_element:
                        capability = th_element.text.strip()
                    else:
                        capability = ''
                    td_elements = row.find_all('td')
                    if len(td_elements) >= 2:
                        function = td_elements[0].text.strip()
                        tools = td_elements[1].text.strip()
                    else:
                        function = ''
                        tools = ''
                    capabilities.append({
                        'capability': capability,
                        'function': function,
                        'tools': tools
                    })
            else:
                # Handle the case where the 'table' element was not found
                print(f"\nProcess exception: {url}--No 'table' element found within the 'capabilities' section")
        else:
            # Handle the case where the 'capabilities' div was not found
            print(f"\nProcess exception: {url}--'capabilities' section not found in the HTML document")

        faqs = []
        faq_section = soup.find('div', {'id': 'accordion-faqs'})
        if faq_section:
            faq_items = faq_section.find_all('div', class_='accordion-item')
            for item in faq_items:
                question = item.find('button', class_='accordion-button').text.strip()
                answer = item.find('div', class_='accordion-body').text.strip()
                faqs.append({
                    'question': question,
                    'answer': answer
                })

        reviews = []
        review_section = soup.find('section', class_='reviews')
        if review_section:
            rating_div = review_section.find('div', class_='d-flex feedbacks')
            if rating_div:
                rating = rating_div.find('div', class_='rating')['data-rating']
                rating_count = rating_div.find('div', class_='rating')['data-rating-count']
                
            review_divs = review_section.find_all('div', class_='py-2')
            for review_div in review_divs:
                reviewer_link = review_div.find('a')
                if reviewer_link:
                    reviewer_name = reviewer_link.text.strip()
                else:
                    reviewer_name_element = review_div.find('h6', class_='fw-semibold mb-0')
                    if reviewer_name_element:
                        reviewer_name = reviewer_name_element.text.strip()
                    else:
                        reviewer_name = ''
                reviewer_role = review_div.find('span', class_='fs-sm text-muted')
                if reviewer_role:
                    reviewer_role = reviewer_role.text.strip()
                else:
                    reviewer_role = ''
                rating_icons = review_div.find_all('i', class_='bx bxs-star text-warning')
                review_rating = len(rating_icons)
                review_text_element = review_div.find('div', class_='fst-italic review-format my-2')
                review_text = review_text_element.text.strip() if review_text_element else ''
                likes_element = review_div.find('span', class_='fs-sm')
                likes_text = likes_element.text.strip() if likes_element else ''
                likes = int(likes_text) if likes_text.isdigit() else 0
                date_element = review_div.find('time')
                date = date_element.get('datetime') if date_element else ''

                review_data = {
                    'reviewer_name': reviewer_name,
                    'reviewer_role': reviewer_role,
                    'rating': review_rating,
                    'review_text': review_text,
                    'likes': likes,
                    'date': date
                }
                reviews.append(review_data)

            try_gpt_link = soup.find('a', class_='btn btn-primary shadow-primary btn-lg my-4')
            if try_gpt_link:
                try_gpt_link_value = try_gpt_link['href']
            else:
                try_gpt_link_value = ''


        info = {
            'name': name,
            'author': author,
            'rating': rating,
            'rating_count': rating_count,
            'rating_max': rating_max,
            'review_count': review_count,
            'chat_count': chat_count,
            'features': features,
            'description': description,
            'tags': tags,
            'release_date': release_date,
            'category': category,
            'update_info': update_info,
            'capabilities': capabilities,
            'share_recipient': share_recipient,
            'official_rating': official_rating,
            'number_of_ratings': rating_count,
            'conversation_starters':conversation_starters,
            'faqs': faqs,
            'reviews': reviews,
            'try_gpt_link': try_gpt_link_value
            
            # 其他键值对...
        }

        return info

    else:
        print(f"Failed to fetch the webpage.")
        return None

def write_to_file(data, output_file):
    with open(output_file, 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2, default=datetime_handler)
    print(f"Information saved to '{output_file}' file.")


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
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


# # 添加命令行参数解析器
# parser = argparse.ArgumentParser(description='Web scraper for GPT apps')
# parser.add_argument('--start', type=int, default=1, help='Starting line number of the links (default: 1)')
# args = parser.parse_args()

# output_dir = 'output'
# os.makedirs(output_dir, exist_ok=True)

# with open("output\\links_unique2.txt", "r", encoding="utf-8") as f:
#     links = f.read().splitlines()

# total_links = len(links)
# start_idx = args.start - 1  # 将起始行号转换为索引

# if start_idx < 0 or start_idx >= total_links:
#     print(f"Invalid starting line number: {args.start}. It should be between 1 and {total_links}.")
#     exit(1)

# for idx in range(start_idx, total_links):
#     url = links[idx]
#     print(f"Processing link {idx + 1}/{total_links}: {url}")
#     info = scrape_gpt_info(url, headers)
#     if info:
#         output_file = os.path.join(output_dir, f"output_info_2.json")
#         with open(output_file, 'a', encoding='utf-8') as file:
#             json.dump(info, file, ensure_ascii=False, indent=2, default=datetime_handler)
#             file.write('\n')  # 在每个JSON对象后添加换行符
#     else:
#         print(f"No information found for link: {url}")

# print("Web scraping completed.")
# 添加命令行参数解析器
parser = argparse.ArgumentParser(description='Web scraper for GPT apps')
parser.add_argument('--file', type=str, required=True, help='The links_unique file to process')
parser.add_argument('--start', type=int, default=1, help='Starting line number of the links (default: 1)')
args = parser.parse_args()

current_dir = os.getcwd()
output_dir = os.path.join(current_dir, 'output')
os.makedirs(output_dir, exist_ok=True)

# 构造要处理的文件路径
links_file = os.path.join(output_dir, args.file)

# 检查文件是否存在
if not os.path.isfile(links_file):
    print(f"Error: File '{args.file}' not found in the '{output_dir}' directory.")
    exit(1)

# 打开要处理的 links_unique*.txt 文件
with open(links_file, "r", encoding="utf-8") as f:
    links = f.read().splitlines()

total_links = len(links)
start_idx = args.start - 1  # 将起始行号转换为索引

if start_idx < 0 or start_idx >= total_links:
    print(f"Invalid starting line number: {args.start}. It should be between 1 and {total_links}.")
    exit(1)

# 获取对应的输出文件名
output_file_name = os.path.splitext(args.file)[0][os.path.splitext(args.file)[0].find('unique') + 6:]
output_file = os.path.join(output_dir, f"output_info_{output_file_name}.json")

for idx in range(start_idx, total_links):
    url = links[idx]
    print(f"{args.file} {idx + 1}/{total_links} --> {url}")
    info = scrape_gpt_info(url, headers)
    if info:
        with open(output_file, 'a', encoding='utf-8') as file:
            json.dump(info, file, ensure_ascii=False, indent=2, default=datetime_handler)
            file.write('\n')  # 在每个JSON对象后添加换行符
    else:
        print(f"No information found for link: {url}")

print(f"Web scraping for {args.file} completed. The information is saved to {output_file}.")