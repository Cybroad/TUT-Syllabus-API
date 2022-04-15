from array import array
import requests
from bs4 import BeautifulSoup
import json
import sys

# args = sys.argv  # 引数を取得
def get_timetable(n):
    dataArray = []
    department = ["BT","CS","MS","ES","ESE5","ESE6","ESE7","X1","DS","HS","HSH1","HSH2","HSH3","HSH4","HSH5","HSH6","X3","GF","GH"]
    json_open = open(department[n]+'_test.json', 'r')
    timeTableData = json.load(json_open)

    num = len(timeTableData)

    for i in range(num):
        val = timeTableData[i]  # 時間割コード取得
        res = requests.get(
            'https://kyo-web.teu.ac.jp/syllabus/2022/' + department[n] + '_' + val + '_ja_JP.html')
        print(i)
        if res.status_code == 404:
            continue
        bs = BeautifulSoup(res.content, 'html.parser')
        table_elements = bs.find_all('table', class_='syllabus-normal')[0]
        titles = table_elements.find_all('th', class_='syllabus-prin')
        tds = table_elements.find_all('td')

        ary = []

        for td in tds:
            ary.append(td.get_text().strip().replace(' ', '').replace(
                '\r\n', '').replace('\u30001', '').replace('\u3000', ''))

        dataArray.append(ary)

        print(dataArray)

    with open(department[n]+'_data.json', 'w') as f:
        json.dump(dataArray, f, ensure_ascii=False, indent=4)