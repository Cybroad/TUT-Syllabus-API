from fastapi import FastAPI
import json

readFileDir = "./lecture_Data"  # 講義データ書き出しフォルダ名指定(相対パス)

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


department = ["BT", "CS", "MS", "ES", "ESE5", "ESE6", "ESE7", "X1", "DS",
              "HS", "HSH1", "HSH2", "HSH3", "HSH4", "HSH5", "HSH6", "X3", "GF", "GH"]

print("> " + str(len(department)) + "個の学部別シラバスデータの取得を開始します")

for i in range(len(department)):
    readFile = open(readFileDir + "/" + department[i] + '.json', 'r')
    for val in json.load(readFile):
        dataLists.append(val)

print("> シラバスデータ取得完了")
print("\n")


@ app.get("/debug/{id}")
def getTimeTableInfo(id: str):
    for i in range(0, len(dataLists)):
        for j in range(0, len(dataLists[i])):
            if serchIndexCheck(dataLists[i][j], id):
                return dataLists[i][9]


@ app.post("/getInfoAll/")
def getTimeTableInfo(data: list[str]):
    ary = 0

    for val in data:
        for i in range(0, len(dataLists)):
            for j in range(0, len(dataLists[i])):
                if serchIndexCheck(dataLists[i][j], val):
                    ary += int(dataLists[i][9])

    return ary
