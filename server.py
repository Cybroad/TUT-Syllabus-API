# ====================================================
# 東京工科大学 単位計算API
#
# 開発元：TUT22 Dev Team (tut22_dev@6mile.dev)
# ====================================================

import settings
from fastapi import FastAPI
import json

dataLists = []
app = FastAPI()

def serchIndex(l, x, default=False):
    if x in l:
        return l.index(x)
    else:
        return default


def serchIndexCheck(l, x):
    if x in l:
        return True
    else:
        return False

print("> " + str(len(settings.department)) + "個の学部別シラバスデータの取得を開始します")

for i in range(len(settings.department)):
    readFile = open(settings.lectureDataDir + "/" + settings.department[i] + '.json', 'r')
    for val in json.load(readFile):
        dataLists.append(val)

print("> シラバスデータ取得完了")
print("\n")


@app.get("/debug/{id}")
def getTimeTableInfo(id: str):
    for i in range(0, len(dataLists)):
        for j in range(0, len(dataLists[i])):
            if serchIndexCheck(dataLists[i][j], id):
                return dataLists[i][9]


@app.post("/getInfoAll/")
def getTimeTableInfo(data:list):
    ary = 0
    print(data)
    for val in data:
        for i in range(0, len(dataLists)):
            for j in range(0, len(dataLists[i])):
                if serchIndexCheck(dataLists[i][j], val):
                    ary += int(dataLists[i][9])

    return ary
