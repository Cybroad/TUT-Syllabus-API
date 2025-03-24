import ujson
import os
import argparse
from get_chrome_driver import GetChromeDriver
from selenium import webdriver
import tqdm

from functions import get_lecture_code, get_timetable

DEPARTMENT = ["BT", "CS", "MS", "ES", "ESE5", "ESE6", "ESE7", "X1", "DS", "HS", "HSH1", "HSH2", "HSH3", "HSH4", "HSH5", "HSH6", "X3", "GF", "GH"]

LECTURE_CODES_FILE = "output/lecture_codes.json"

def _driver_init():
    get_driver = GetChromeDriver()
    get_driver.install()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)

def _get_lecture_code():
    lecture_codes = {}
    print("Start getting lecture codes.")
    for dept in tqdm.tqdm(DEPARTMENT):
        # 指定学部の講義コードを取得
        lecture_codes[dept] = get_lecture_code.get_lecture_code(dept, _driver_init)
        
        # 講義コード取得失敗時
        if lecture_codes == None:
            print(f"Failed to get {dept} lecture codes.")
            print('Skip to get lecture data.')
            continue

    with open(LECTURE_CODES_FILE, 'w') as f:
        ujson.dump(lecture_codes, f, ensure_ascii=False, indent=4)

def _get_lecture_data(department):
    if not os.path.exists(LECTURE_CODES_FILE):
        print("Failed to get lecture data: lecture_codes.json is not found.")
        return
    
    with open(LECTURE_CODES_FILE, 'r') as f:
        lecture_codes = ujson.load(f)

    print(f"Getting {department} lecture data.")

    if lecture_codes[department] == None:
        print(f"Since {department} is not in lecture_codes, skip to get lecture data.")
        return
    
    os.makedirs(f"output/{department}", exist_ok=True)
    for lecture_code in lecture_codes[department]:
        lecture_data = get_timetable.get_timetable(department, lecture_code)

        if lecture_data == None:
            print(f"Failed to get {department} lecture data: {lecture_code}")
            continue

        with open(f"output/{department}/{lecture_code}.json", 'w') as f:
            ujson.dump(lecture_data, f, ensure_ascii=False, indent=4, encode_html_chars=True)

        print(f"Successfully got {department} lecture data: {lecture_code}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', required=True, choices=["lecture_codes", "lecture_data"])
    parser.add_argument('-d', '--department', choices=DEPARTMENT)
    args = parser.parse_args()

    if args.type == "lecture_data" and not args.department:
        parser.error("--department is required when type is lecture_data")

    for directory in ["docs", "docs/api", "docs/api/v1", "output"]:
        os.makedirs(directory, exist_ok=True)

    if args.type == "lecture_codes":
        _get_lecture_code()

    if args.type == "lecture_data":
        _get_lecture_data(args.department)
