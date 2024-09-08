# ====================================================
# 東京工科大学 学内シラバス API
# ====================================================
from time import sleep
from functions import get_lecture_code, get_lecture_data
import os
import json

# データ取得先学部指定
#department = ["BT", "CS", "MS", "ES", "ESE5", "ESE6", "ESE7", "X1", "DS", "HS", "HSH1", "HSH2", "HSH3", "HSH4", "HSH5", "HSH6", "X3", "GF", "GH"]
department = ["BT","CS"]
# ※教養科目の"X1"は必須

os.makedirs("docs", exist_ok=True)
os.makedirs("docs/api", exist_ok=True)
os.makedirs("docs/api/v1", exist_ok=True)

for dept in department:
    os.makedirs(f"docs/api/v1/{dept}", exist_ok=True)
    # 指定学部の講義コードを取得
    lecture_codes = get_lecture_code.get_lecture_code(dept)
    for lecture_code in lecture_codes:
        # 講義データを取得
        sleep(1)
        lecture_data = get_lecture_data.get_timetable(dept, lecture_code)
        if lecture_data:
            with open(f"docs/api/v1/{dept}/{lecture_code}.json", "w") as f:
                json.dump(lecture_data, f, ensure_ascii=False, indent=4)
