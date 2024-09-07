# ------------------------------------------
# 時間割コード及び講義データ取得ファイル
# ※ 各種パス等は[.setting.py]を参照
# ------------------------------------------

# ===========================================================================
# 時間割コード取得関数
# ===========================================================================
from bs4 import BeautifulSoup
import requests
import settings
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import json
import ssl, urllib3

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

def fetch_syllabus(url: str):
    session = requests.session()
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4
    session.mount('https://', CustomHttpAdapter(ctx))
    res = session.get(url)
    return res


def getcode(v):
    def getPageNum():  # 現在のページ数及び全体ページ数取得関数
        mPageN_o = driver.find_element(By.XPATH,  # エレメント抽出
                                       '/html/body/form/div[2]/p[1]').text
        conditons = r'\全部で .*\あります'  # 任意の条件を設定
        mPageN_a = re.findall(conditons, mPageN_o)  # 条件にマッチする文字列を取得
        mPageN = int(mPageN_a[0].replace(
            '全部で ', '').replace('件あります', ''))  # 全体ページ数
        cPageN_o = driver.find_element(By.XPATH,  # エレメント抽出
                                       '/html/body/form/div[2]/p[1]/b[2]').text
        cPageN = int(cPageN_o.replace("件目", ''))  # 現在のページ数

        return cPageN, mPageN  # p[0]:現在のページ数, p[1]:全体ページ数

    # =========================================================================

    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=options
    )
    array = []
    driver.get("https://kyo-web.teu.ac.jp/campussy/")  # アクセスするURL

    driver.switch_to.frame(driver.find_element(
        By.NAME, "search"))  # 検索フレームを切り替える

    print("...取得中")
    Select(driver.find_element(By.ID, 'jikanwariShozokuCode')
           ).select_by_value(v)  # コンピュータサイエンス学部

    Select(driver.find_element(By.NAME, '_displayCount')
           ).select_by_value('200')  # 一覧表示件数

    driver.find_elements(By.XPATH,
                         '//*[@id = "jikanwariKeywordForm"]/table[2]/tbody/tr/td/table/tbody/tr[9]/td/input[1]')[0].click()  # 検索ボタンをクリック

    driver.switch_to.default_content()  # 検索フレームをもとに戻す

    driver.switch_to.frame(
        driver.find_element(By.NAME, "result"))  # 検索結果フレームを切り替える

    thNum = len(driver.find_elements(By.XPATH,
                                     '/html/body/form/div[2]/table/tbody/tr'))  # エレメント数取得

    for num in range(1, thNum):
        array.append(driver.find_element(By.XPATH,
                                         '/html/body/form/div[2]/table/tbody/tr[' + str(num) + ']/td[4]').text)

    p = getPageNum()  # 現在のページ数及び全体ページ数取得関数を実行
    aTagN = int(len(driver.find_elements(By.XPATH,
                                         '/html/body/form/div[2]/p[1]/a'))) - 1

    if (aTagN > 0):
        driver.find_elements(By.XPATH,
                             '/html/body/form/div[2]/p[1]/a')[aTagN].click()  # 次ページをクリック

        while p[0] < p[1]:  # 現在のページ数が全体ページ数より小さい間

            p = getPageNum()  # 現在のページ数及び全体ページ数取得関数を実行

            driver.switch_to.default_content()  # 検索フレームをもとに戻す

            driver.switch_to.frame(
                driver.find_element(By.NAME, "result"))  # 検索結果フレームを切り替える

            thNum = len(driver.find_elements(By.XPATH,
                                             '/html/body/form/div[2]/table/tbody/tr'))  # エレメント数取得

            for num in range(1, thNum):
                array.append(driver.find_element(By.XPATH,
                                                 '/html/body/form/div[2]/table/tbody/tr[' + str(num) + ']/td[4]').text)

            aTagN = len(driver.find_elements(By.XPATH,
                                             '/html/body/form/div[2]/p[1]/a')) - 1

            driver.find_elements(By.XPATH,
                                 '/html/body/form/div[2]/p[1]/a')[aTagN].click()  # 次ページをクリック

    driver.quit()

    with open(settings.timeTableCodeDir + "/" + v + '.json', 'w') as f:
        json.dump(array, f, ensure_ascii=False, indent=4)
    return "finish"


# ===========================================================================
# 講義データ取得関数 (時間割コード => 授業内容等(単位数))
# ===========================================================================


def get_timetable(v):
    dataArray = []
    json_open = open(settings.timeTableCodeDir + "/" + v + '.json', 'r')
    timeTableData = json.load(json_open)

    num = len(timeTableData)
    print("...取得中")
    for i in range(num):
        val = timeTableData[i]  # 時間割コード取得
        print(val)

        if v == "﻿BT":
            res = fetch_syllabus('https://kyo-web.teu.ac.jp/syllabus/2024/' + 'BT' + '_' + val + '_ja_JP.html')
        else:
            res = fetch_syllabus('https://kyo-web.teu.ac.jp/syllabus/2024/' + v + '_' + val + '_ja_JP.html')
        
        if res.status_code == 404:
            continue
        bs = BeautifulSoup(res.content, 'html.parser')
        table_elements = bs.find_all('table', class_='syllabus-normal')[0]
        tds = table_elements.find_all('td')

        ary = []

        for td in tds:
            ary.append(td.get_text().strip().replace(' ', '').replace(
                '\r\n', '').replace('\u30001', '').replace('\u3000', ''))

        dataArray.append(ary)

    with open(settings.lectureDataDir + "/" + v + '.json', 'w') as f:
        json.dump(dataArray, f, ensure_ascii=False, indent=4)
