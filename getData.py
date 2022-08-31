from array import array
import requests
from bs4 import BeautifulSoup
import json

# =============================================================================
# 初期設定項目
# =============================================================================

readFileDir = "./timeTableId_Data"  # 読み込むフォルダ名を設定(相対パス)
writeFileDir = "./lecture_Data"  # 講義データ書き出しフォルダ名指定(相対パス)

# =============================================================================


def get_timetable(n):
    dataArray = []
    department = ["CS", "MS"]
    json_open = open(readFileDir + "/" + department[n]+'.json', 'r')
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

    with open(writeFileDir + "/" + department[n]+'.json', 'w') as f:
        json.dump(dataArray, f, ensure_ascii=False, indent=4)
