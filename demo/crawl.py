import time
import random
import requests
from datetime import datetime
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

# udn 聯合新聞網，不同網頁版型範例
# https://udn.com/news/story/6809/4690414
# https://udn.com/news/story/6904/4698001   # https://udn.com/umedia/story/12762/4697096
# https://udn.com/news/story/6809/4699983   # https://global.udn.com/global_vision/story/8663/4698371
# https://udn.com/news/story/6809/4699958   # https://opinion.udn.com/opinion/story/120611/4698526
# https://udn.com/news/story/6812/4700330   # 跳轉"會員專屬內容"


def get_news_list(page_num=3):
    """爬取新聞列表"""
    base_url = "https://udn.com/api/more"

    news_list = []
    for page in range(page_num):
        channelId = 1
        cate_id = 0
        type_ = 'breaknews'
        query = f"page={page+1}&channelId={channelId}&cate_id={cate_id}&type={type_}"
        news_list_url = base_url + '?' + query
        print(news_list_url)
        # https://udn.com/api/more?page=2&channelId=1&cate_id=0&type=breaknews
        
        r = requests.get(news_list_url, headers=HEADERS)
        news_data = r.json()
        news_list.extend(news_data['lists'])

        # time.sleep(random.uniform(1, 2))

    return news_list

def get_content(news):
    try:
        url = f"https://udn.com{news['titleLink']}"
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        article = soup.find(class_="article-content__editor")
        
        p_tags = article.find_all("p")
        content = ""
        for p in p_tags:
            figures = p.find_all("figure")
            for figure in figures:
                figure.decompose()

        for p in p_tags:
            content += p.text
            content += "\n"

        ret = {
            "title": news["title"],
            "url": url,
            "view": news["view"],
            "time": news["time"],
            "content": content
        }
        return ret
    except:
        return None

if __name__ == "__main__":
    news_list = get_news_list(page_num=2)
    print(news_list[-1])
    print(f"共抓到 {len(news_list)} 篇新聞")    
    # with open("urls.json", "r") as f:
    #     news_list = json.load(f)
    result = []
    print(type(news_list))
    for i, news in enumerate(tqdm(news_list[:6])):
        ret = get_content(news)
        # print(ret)
        if ret != None:
            result.append(ret)
    now = str(datetime.now())
    now = now.split(".")[0]
    now = now.replace("-", "_")
    now = now.replace(":", "_")
    with open(f"{now}.json", "w") as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=2))


# 其他更多
# 即時-不分類
# channelId: 1
# cate_id: 99
# type: breaknews

# 即時-精選
# channelId: 1
# cate_id: 0
# type: breaknews

# 即時-地方
# channelId: 1
# cate_id: 3
# type: breaknews

# 運動-最新
# channelId: 2
# type: cate_latest_news
# cate_id: 7227

# 運動-棒球
# channelId: 2
# type: subcate_articles
# cate_id: 7227
# sub_id: 7001

# 運動-NBA
# channelId: 2
# type: subcate_articles
# cate_id: 7227
# sub_id: 7002

# 生活-最新
# channelId: 2
# type: cate_latest_news
# cate_id: 6649

# 生活-星座
# channelId: 2
# type: subcate_articles
# cate_id: 6649
# sub_id: 7268
# totalRecNo: 363

# 數位-最新
# channelId: 2
# type: cate_latest_news
# cate_id: 7226

# 數位-焦點
# channelId: 2
# type: subcate_articles
# cate_id: 7226
# sub_id: 7086
# is_paywall: 0
# is_bauban: 0
# is_vision: 0