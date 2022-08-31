# ====================================================
# 東京工科大学 学内シラバス 科目情報取得ツール
#
# 開発元：TUT22 Dev Team (tut22_dev@6mile.dev)
# ====================================================
import getData
import settings

for i in settings.department:
    print("> " + i + " 学部の時間割コードの取得を開始します")
    x = getData.getcode(i)
    if x == "finish":
        print("> " + i + " 学部の時間割コードの取得が完了しました")
        print("> " + i + " 学部の講義データの取得を開始します")
        getData.get_timetable(i)
        print("> " + i + " 学部の講義データの取得が完了しました")

print("> 指定されたすべての学部のデータ取得が完了しました")