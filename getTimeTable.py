from lib2to3.pgen2 import driver
from locale import currency
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.support.select import Select
import re
import json
import sys

args = sys.argv  # 引数を取得


driver = webdriver.Chrome(
    executable_path='C:\chromedriver_win32\\chromedriver.exe')

array = []

driver.get("https://kyo-web.teu.ac.jp/campussy/")  # アクセスするURL

driver.switch_to.frame(driver.find_element_by_name("search"))  # 検索フレームを切り替える

Select(driver.find_element_by_id('jikanwariShozokuCode')
       ).select_by_value(args[1])  # コンピュータサイエンス学部

Select(driver.find_element_by_name('_displayCount')
       ).select_by_value('200')  # 一覧表示件数

driver.find_elements_by_xpath(
    '//*[@id = "jikanwariKeywordForm"]/table[2]/tbody/tr/td/table/tbody/tr[9]/td/input[1]')[0].click()  # 検索ボタンをクリック

driver.switch_to.default_content()  # 検索フレームをもとに戻す

driver.switch_to.frame(driver.find_element_by_name("result"))  # 検索結果フレームを切り替える

thNum = len(driver.find_elements_by_xpath(
    '/html/body/form/div[2]/table/tbody/tr'))  # エレメント数取得

print("エレメント " + str(thNum))

for num in range(1, thNum):
    array.append(driver.find_element_by_xpath(
        '/html/body/form/div[2]/table/tbody/tr[' + str(num) + ']/td[4]').text)

# ==========================================================
# 現在のページ数及び全体ページ数取得
# ==========================================================


def getPageNum():  # 現在のページ数及び全体ページ数取得関数
    mPageN_o = driver.find_element_by_xpath(  # エレメント抽出
        '/html/body/form/div[2]/p[1]').text
    conditons = r'\全部で .*\あります'  # 任意の条件を設定
    mPageN_a = re.findall(conditons, mPageN_o)  # 条件にマッチする文字列を取得
    mPageN = int(mPageN_a[0].replace(
        '全部で ', '').replace('件あります', ''))  # 全体ページ数
    cPageN_o = driver.find_element_by_xpath(  # エレメント抽出
        '/html/body/form/div[2]/p[1]/b[2]').text
    cPageN = int(cPageN_o.replace("件目", ''))  # 現在のページ数

    return cPageN, mPageN  # p[0]:現在のページ数, p[1]:全体ページ数


p = getPageNum()  # 現在のページ数及び全体ページ数取得関数を実行

aTagN = int(len(driver.find_elements_by_xpath(
    '/html/body/form/div[2]/p[1]/a'))) - 1

if(aTagN > 0):
    driver.find_elements_by_xpath(
        '/html/body/form/div[2]/p[1]/a')[aTagN].click()  # 次ページをクリック

    while p[0] < p[1]:  # 現在のページ数が全体ページ数より小さい間

        p = getPageNum()  # 現在のページ数及び全体ページ数取得関数を実行

        driver.switch_to.default_content()  # 検索フレームをもとに戻す

        driver.switch_to.frame(
            driver.find_element_by_name("result"))  # 検索結果フレームを切り替える

        thNum = len(driver.find_elements_by_xpath(
            '/html/body/form/div[2]/table/tbody/tr'))  # エレメント数取得

        for num in range(1, thNum):
            array.append(driver.find_element_by_xpath(
                '/html/body/form/div[2]/table/tbody/tr[' + str(num) + ']/td[4]').text)

        aTagN = len(driver.find_elements_by_xpath(
            '/html/body/form/div[2]/p[1]/a')) - 1

        driver.find_elements_by_xpath(
            '/html/body/form/div[2]/p[1]/a')[aTagN].click()  # 次ページをクリック

driver.quit()

with open('test.json', 'w') as f:
    json.dump(array, f, ensure_ascii=False, indent=4)
