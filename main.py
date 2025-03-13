# ====================================================
# 開発環境用のスクリプト
# ====================================================
from functions import get_lecture_code, get_timetable
import os
import tqdm
import json
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options

# データ取得先学部指定
department = ["BT", "CS", "MS", "ES", "ESE5", "ESE6", "ESE7", "X1", "DS", "HS", "HSH1", "HSH2", "HSH3", "HSH4", "HSH5", "HSH6", "X3", "GF", "GH"]
# ※教養科目の"X1"は必須

# 定数設定
SELENIUM_DRIVER_PATH = 'http://localhost:4444/wd/hub'

def driver_init():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')

    # コンテナが起動しているか確認
    try:
        driver = Remote(command_executor=SELENIUM_DRIVER_PATH, options=options)
    except:
        print("Selenium Grid is not running.")
        print("Please run the following command.")
        print("docker-compose up -d")
        exit()

    return driver

os.makedirs("docs", exist_ok=True)
os.makedirs("docs/api", exist_ok=True)
os.makedirs("docs/api/v1", exist_ok=True)
os.makedirs("output", exist_ok=True)


# Step1: 学部ごとの講義コードを取得
is_skip_fetch_flag = False
# もし、jsonファイルが存在する場合は、取得済みの講義コードを読み込む
if os.path.exists("output/lecture_codes.json"):
    with open("output/lecture_codes.json", 'r') as f:
        lecture_codes = json.load(f)
        is_skip_fetch_flag = True
else:
    lecture_codes = {}

if is_skip_fetch_flag:
    print("Skip to get lecture codes.")
else:
    print("Start getting lecture codes.")
    for dept in tqdm.tqdm(department):
        os.makedirs(f"docs/api/v1/{dept}", exist_ok=True)
        # 指定学部の講義コードを取得
        lecture_codes[dept] = get_lecture_code.get_lecture_code(dept, driver_init)
        
        # 講義コード取得失敗時
        if lecture_codes == None:
            print(f"Failed to get {dept} lecture codes.")
            print('Skip to get lecture data.')
            continue

    # 講義コードをjsonファイルに保存
    with open("output/lecture_codes.json", 'w') as f:
        json.dump(lecture_codes, f, ensure_ascii=False, indent=4)

    
# Step2: 講義データを取得
print("Start getting lecture data.")
for dept in department:
    if lecture_codes[dept] == None:
        continue

    print(f"Getting {dept} lecture data.")

    for lecture_code in lecture_codes[dept]:
        lecture_data = get_timetable.get_timetable(dept, lecture_code)
        if lecture_data == None:
            print(f"Failed to get {dept} lecture data: {lecture_code}")
            continue

        with open(f"docs/api/v1/{dept}/{lecture_code}.json", 'w') as f:
            json.dump(lecture_data, f, ensure_ascii=False, indent=4)

        print(f"Successfully got {dept} lecture data: {lecture_code}")
