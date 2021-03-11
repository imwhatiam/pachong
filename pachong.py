import re
import time
import requests

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
headers = {
    'User-Agent': user_agent
}

group_id = '628580'
start = 0

while start < 500:
    time.sleep(5)
    url = "https://www.douban.com/group/{}/discussion?start={}".format(group_id, start)
    start += 25

    r = requests.get(url, headers=headers)

    file_name = 'discussion?start={}.html'.format(start)

    with open(file_name, 'w') as f:
        f.write(r.text)

    lines = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if 'https://www.douban.com/group/topic/' in line:
                lines.append(line.strip())

    regex = '.*href="(.*)" title="(.*)" class.*'

    with open('result.md', 'a') as f:
        for line in lines:
            match = re.match(regex, line)
            if match:
                f.write('[{}]({})'.format(match.group(2), match.group(1)) + '\n\n')
