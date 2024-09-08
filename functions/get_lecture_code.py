from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import re

# 定数設定
SELENIUM_DRIVER_PATH = 'http://localhost:4444/wd/hub'
TUT_CAMPUSSY_URL = 'https://kyo-web.teu.ac.jp/campussy/'
VIEW_RESULT_COUNT = '200'

# オプション設定
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')


# 現在のページ数及び全体ページ数を取得する関数
def get_search_result_page_num(driver: webdriver.Remote) -> dict:
    # 検索結果の件数を表示するエレメントを取得
    search_result_count_element = driver.find_element(By.XPATH, '/html/body/form/div[2]/p[1]').text

    # 検索結果件数のテキスト部分を抽出
    search_result_count_list =  re.findall(r'\全部で .*\あります', search_result_count_element) 

    # 抽出結果が0件の場合は、0を返す
    if len(search_result_count_list) == 0:
        return {
            'current_page_result_count': 0,
            'total_page_result_count': 0
        }
    
    # 全体ページ数を取得
    search_result_count_all = int(search_result_count_list[0].replace('全部で ', '').replace('件あります', ''))

    # 現在のページ数を取得
    current_page_count_element = driver.find_element(By.XPATH, '/html/body/form/div[2]/p[1]/b[2]').text
    current_page_count = int(current_page_count_element.replace("件目", ''))

    return {
        'current_page_result_count': current_page_count,
        'total_page_result_count': search_result_count_all
    }

def get_lecture_code_list_from_search_result_element(driver: webdriver.Remote) -> list[str]:
    # 検索結果の件数を取得
    th_tags_elements = driver.find_elements(By.XPATH, '/html/body/form/div[2]/table/tbody/tr')

    # 時間割コードを格納するリスト
    lecture_code_list = []
    for i in enumerate(th_tags_elements):
        lecture_code_list.append(driver.find_element(By.XPATH, f'/html/body/form/div[2]/table/tbody/tr[{str(i[0]+1)}]/td[4]').text)

    return lecture_code_list


# 学外シラバスから時間割コードを取得する関数
# @param: 取得対象の学部名
def get_lecture_code(department_name: str) -> list[str]:
    driver = webdriver.Remote(
        command_executor=SELENIUM_DRIVER_PATH,
        options=options
    )

    driver.get(TUT_CAMPUSSY_URL)

    # 検索条件のiframeに切り替え
    driver.switch_to.frame(driver.find_element(By.NAME, "search"))

    # 学部選択
    # ※応用生物学部(BT)の場合は、先頭に特殊文字を入れないと選択できない
    if department_name == "BT":
        Select(driver.find_element(By.ID, 'jikanwariShozokuCode')).select_by_value("﻿BT")
    else:
        Select(driver.find_element(By.ID, 'jikanwariShozokuCode')).select_by_value(department_name)

    # 一覧表示件数を200件(最大値)に変更
    Select(driver.find_element(By.NAME, '_displayCount')
           ).select_by_value(VIEW_RESULT_COUNT)
    
    # 検索ボタンをクリック
    search_button = driver.find_elements(By.XPATH,'//*[@id = "jikanwariKeywordForm"]/table[2]/tbody/tr/td/table/tbody/tr[9]/td/input[1]')[0]
    search_button.click()

    # 検索条件のiframeから抜ける
    driver.switch_to.default_content()

    # 検索結果のiframeに切り替え
    driver.switch_to.frame(driver.find_element(By.NAME, "result"))

    # 現在のページ数及び全体ページ数を取得
    page_data = get_search_result_page_num(driver)

    # 全体ページ数が0の場合、ドライバーを閉じて時間割コードリストを返す
    if page_data['total_page_result_count'] == 0:
        driver.quit()
        return None
    
    # 時間割コードを格納するリスト
    lecture_code_list = []

    # ページ数
    total_page = int(page_data['total_page_result_count'] / page_data['current_page_result_count']) + 1
    
    for i in range(0, total_page):
        lecture_code_list.extend(get_lecture_code_list_from_search_result_element(driver))

        # 次のページがある場合、次ページに遷移
        if page_data['current_page_result_count'] < page_data['total_page_result_count']:
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.NAME, "result"))
            driver.find_elements(By.XPATH, '/html/body/form/div[2]/p[1]/a')[-1].click()

    driver.quit()
    return lecture_code_list

if __name__ == "__main__":
    res = get_lecture_code('MS')
    print(f"{len(res)}件の時間割コードを取得しました")
