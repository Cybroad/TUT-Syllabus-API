from lib2to3.pgen2 import driver
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome(
    executable_path='C:\chromedriver_win32\\chromedriver.exe')

array = []

driver.get("https://kyo-web.teu.ac.jp/campussy/")  # アクセスするURL

driver.switch_to.frame(driver.find_element_by_name("search"))  # 検索フレームを切り替える

Select(driver.find_element_by_id('jikanwariShozokuCode')
       ).select_by_value('CS')  # コンピュータサイエンス学部

Select(driver.find_element_by_name('_displayCount')
       ).select_by_value('200')  # 一覧表示件数

driver.find_elements_by_xpath(
    '//*[@id = "jikanwariKeywordForm"]/table[2]/tbody/tr/td/table/tbody/tr[9]/td/input[1]')[0].click()  # 検索ボタンをクリック

driver.switch_to.default_content()  # 検索フレームをもとに戻す

driver.switch_to.frame(driver.find_element_by_name("result"))  # 検索結果フレームを切り替える

for num in range(1, 100):
    array.append(driver.find_element_by_xpath(
        '/html/body/form/div[2]/table/tbody/tr[' + str(num) + ']/td[4]').text)  # 検索結果を表示

print(array)
