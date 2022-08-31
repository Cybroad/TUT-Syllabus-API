from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import json

options = Options()
options.headless = True

# =============================================================================
# 初期設定項目
# =============================================================================
writeFileDir = "./timeTableId_Data"  # 時間割コードを書き出すフォルダ名を設定(相対パス)

# =============================================================================
def getcode(n):
    driver = webdriver.Chrome("/usr/bin/chromedriver")
    array = []
    department = ["CS", "MS"]
    driver.get("https://kyo-web.teu.ac.jp/campussy/")  # アクセスするURL

    driver.switch_to.frame(driver.find_element(By.NAME, "search"))  # 検索フレームを切り替える

    Select(driver.find_element(By.ID, 'jikanwariShozokuCode')
           ).select_by_value(department[n])  # コンピュータサイエンス学部

    Select(driver.find_element(By.NAME, '_displayCount')
           ).select_by_value('200')  # 一覧表示件数

    driver.find_elements(By.XPATH,
        '//*[@id = "jikanwariKeywordForm"]/table[2]/tbody/tr/td/table/tbody/tr[9]/td/input[1]')[0].click()  # 検索ボタンをクリック

    driver.switch_to.default_content()  # 検索フレームをもとに戻す

    driver.switch_to.frame(
        driver.find_element(By.NAME, "result"))  # 検索結果フレームを切り替える

    thNum = len(driver.find_elements(By.XPATH,
        '/html/body/form/div[2]/table/tbody/tr'))  # エレメント数取得

    print("エレメント数：" + str(thNum))

    for num in range(1, thNum):
        array.append(driver.find_element(By.XPATH,
            '/html/body/form/div[2]/table/tbody/tr[' + str(num) + ']/td[4]').text)

    # ==========================================================
    # 現在のページ数及び全体ページ数取得
    # ==========================================================

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

    p = getPageNum()  # 現在のページ数及び全体ページ数取得関数を実行

    aTagN = int(len(driver.find_elements(By.XPATH,
        '/html/body/form/div[2]/p[1]/a'))) - 1

    if(aTagN > 0):
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

    with open(writeFileDir + "/" + department[n]+'.json', 'w') as f:
        json.dump(array, f, ensure_ascii=False, indent=4)
        print("finish")
    return "finish"