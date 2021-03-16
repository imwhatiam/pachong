import os
import time
import sqlite3
import requests
from bs4 import BeautifulSoup
# import re
# from pprint import pprint

db_name = 'result.db'

if not os.path.exists(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS topic (
            topic_url TEXT PRIMARY KEY,
            title TEXT,
            count INTEGER DEFAULT 0,
            last_reply TEXT DEFAULT '',
            create_time TEXT DEFAULT '',
            content TEXT DEFAULT '',
            image_url TEXT DEFAULT '');
        ''')
    con.commit()
else:
    con = sqlite3.connect(db_name)
    cur = con.cursor()


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.3'

headers = {
    'User-Agent': user_agent
}

group_id = '628580'
start = 0

with open('result.md', 'w') as f:

    f.write('|title|count|last reply|\n')
    f.write('|-----|-----|----------|\n')

    while start < 500:

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

            if row.find('span', attrs={'class': 'elite_topic_lable'}):

                a = row.find('a', href=True)
                topic_url = a['href']
                title = a['title']
                count = row.find('td', attrs={'class': 'r-count'}).text
                last_reply = row.find('td', attrs={'class': 'time'}).text

                if '193662234' in topic_url:
                    continue

                select_sql = "SELECT * FROM topic WHERE topic_url='{}'".format(topic_url)
                cur.execute(select_sql)
                if len(cur.fetchall()) > 0:
                    continue

                insert_sql = "INSERT INTO topic VALUES ('{}','{}',{},'{}','','','');".format(topic_url,
                                                                                             title,
                                                                                             count or 0,
                                                                                             last_reply)
                try:
                    cur.execute(insert_sql)

                    f.write('|[{}]({})|{}|{}|\n'.format(title.replace('|', ','),
                                                        topic_url,
                                                        count or 0,
                                                        last_reply))

                except Exception as e:
                    print(e)
                    print(insert_sql)

con.commit()
con.close()
