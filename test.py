import json
import sys
from unittest import result

args = sys.argv

department = 19

readFileDir = "./lecture_Data"  # 講義データ書き出しフォルダ名指定(相対パス)

dataLists = []


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

for i in range(0, len(dataLists)):
    for j in range(0, len(dataLists[i])):
        if serchIndexCheck(dataLists[i][j], args[1]):
            print("時間割コード： " + args[1])
            print(dataLists[i][0] + " の" + "単位数は " + dataLists[i][9] + " です")
