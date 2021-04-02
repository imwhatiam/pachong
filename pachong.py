# -*- coding: utf-8 -*-
import os
import time
import requests
from bs4 import BeautifulSoup
# import re
# from pprint import pprint

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.3'

headers = {
    'User-Agent': user_agent
}

group_id = '628580'
start = 0

result_md = 'result.md'

skipped_list = ['193662234', '198931411']

content = ''
if os.path.exists(result_md):
    with open('result.md', 'r') as f:
        content = f.read()

with open(result_md, 'w') as f:

    f.write('|标题|评论数|最后评论时间|本次新增|精华帖|\n')
    f.write('|----|------|------------|--------|------|\n')

    while start < 300:

        time.sleep(5)
        url = "https://www.douban.com/group/{}/discussion?start={}".format(group_id, start)
        start += 25
        print(url)

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        table = soup.find('table', attrs={'class': 'olt'})
        if not table:
            continue

        rows = table.find_all('tr')
        if not rows:
            continue

        for row in rows:

            if 'class="th"' in str(row):
                continue

            good = False
            if row.find('span', attrs={'class': 'elite_topic_lable'}):
                good = True

            try:
                a = row.find('a', href=True)
                topic_url = a['href']
                title = a['title']
                count = row.find('td', attrs={'class': 'r-count'}).text
                last_reply = row.find('td', attrs={'class': 'time'}).text

                should_continue = False
                for item in skipped_list:
                    if item in topic_url:
                        should_continue = True
                        break

                if should_continue:
                    continue

                is_new = True
                if topic_url in content:
                    is_new = False

                f.write('|[{}]({})|{}|{}|{}|{}|\n'.format(title.replace('|', ','),
                                                          topic_url,
                                                          count or 0,
                                                          last_reply,
                                                          'Yes' if is_new else '',
                                                          'Yes' if good else '',))

            except Exception as e:
                print(row)
                print(e)
