from array import array
import requests
from bs4 import BeautifulSoup
import json
import sys

args = sys.argv  # 引数を取得

dataArray = []

json_open = open('./test.json', 'r')
timeTableData = json.load(json_open)

num = len(timeTableData)

for i in range(num):
    val = timeTableData[i]  # 時間割コード取得
    res = requests.get(
        'https://kyo-web.teu.ac.jp/syllabus/2022/' + args[1] + '_' + val + '_ja_JP.html')
    bs = BeautifulSoup(res.content, 'html.parser')
    print(val)

table_elements = bs.find_all('table', class_='syllabus-normal')[0]
titles = table_elements.find_all('th', class_='syllabus-prin')
tds = table_elements.find_all('td')

for td in tds:
    ary = []
    ary.append(td.get_text().strip().replace(
        ' ', '').replace('\r\n', '').replace('\u30001', '').replace('\u3000', ''))
    for td in tds:
        dataArray.append(ary)

with open('data.json', 'w') as f:
    json.dump(array, f, ensure_ascii=False, indent=4)
