# ====================================================
# 東京工科大学 学内シラバス API
#
# 開発元：TUT22 Dev Team (tut22_dev@6mile.dev)
# ====================================================
import getData
import settings
from fastapi import FastAPI
import json
import uvicorn
import os

dataLists = []
app = FastAPI()


if (len(os.listdir(settings.timeTableCodeDir)) == 0 and len(os.listdir(settings.lectureDataDir)) == 0):
    for i in settings.department:
        print("> " + i + " 学部の時間割コードの取得を開始します")
        x = getData.getcode(i)

        if x == "finish":
            print("> " + i + " 学部の時間割コードの取得が完了しました")
    for i in settings.department:
        print(f"> {i}の講義データの取得を開始します")
        x = getData.get_timetable(i)
        if x == "finish":
            print(f"> {i}の講義データの取得が完了しました")

    print("> 指定されたすべての学部のデータ取得が完了しました")


def serchIndexCheck(l, x):
    if x in l:
        return True
    else:
        return False


print("> " + str(len(settings.department)) + "個の学部別シラバスデータの取得を開始します")

for i in range(len(settings.department)):
    readFile = open(settings.lectureDataDir + "/" +
                    settings.department[i] + '.json', 'r')
    for val in json.load(readFile):
        dataLists.append(val)

print("> シラバスデータ取得完了")


@app.post("/debug/{id}")
def getTimeTableInfo(id: str):
    for i in range(0, len(dataLists)):
        for j in range(0, len(dataLists[i])):
            if serchIndexCheck(dataLists[i][j], id):
                return dataLists[i][9]


@app.post("/getInfoAll/")
def getTimeTableInfo(data: list):
    ary = 0
    print(data)
    for val in data:
        for i in range(0, len(dataLists)):
            for j in range(0, len(dataLists[i])):
                # 講義情報データから講義コードを検索(全部の学部データから広域検索)
                if serchIndexCheck(dataLists[i][j], val):
                    if val == dataLists[i][4]:  # 時間割コードと完全一致した場合
                        ary += int(dataLists[i][9])

    return ary


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
