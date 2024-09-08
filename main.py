# ====================================================
# 東京工科大学 学内シラバス API
# ====================================================
from functions import get_lecture_code, get_lecture_data

# データ取得先学部指定
#department = ["BT", "CS", "MS", "ES", "ESE5", "ESE6", "ESE7", "X1", "DS", "HS", "HSH1", "HSH2", "HSH3", "HSH4", "HSH5", "HSH6", "X3", "GF", "GH"]
department = ["BT"]
# ※教養科目の"X1"は必須

for dept in department:
    # 指定学部の講義コードを取得
    lecture_codes = get_lecture_code.get_lecture_code(dept)
    for lecture_code in lecture_codes:
        # 講義データを取得
        lecture_data = get_lecture_data.get_timetable(dept, lecture_code)
        if lecture_data:
            print(lecture_data)
