# ====================================================
# 東京工科大学 学内シラバス 科目情報取得ツール
#
# 開発元：TUT22 Dev Team (tut22_dev@6mile.dev)
# ====================================================
import getTimeTable
import getData
department = 2
for i in range(department):
    print(i)
    x = getTimeTable.getcode(i)
    if x == "finish":
         getData.get_timetable(i)