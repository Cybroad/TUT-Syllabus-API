import json
import sys
from unittest import result

args = sys.argv

department = 19

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


department = ["﻿BT", "CS", "MS", "ES", "ESE5", "ESE6", "ESE7", "X1", "DS",
              "HS", "HSH1", "HSH2", "HSH3", "HSH4", "HSH5", "HSH6", "X3", "GF", "GH"]


for i in range(len(department)):
    print(department[i])
    readFile = open(department[i] + '.json', 'r')
    dataLists.append(json.load(readFile))


print(dataLists)

""" print("> " + str(department) + "個の学部別シラバスデータの取得を開始します")

BT_f = open('BT_data.json', 'r')
BT = json.load(BT_f)

CS_f = open('CS_data.json', 'r')
CS = json.load(CS_f)

MS_f = open('MS_data.json', 'r')
MS = json.load(MS_f)

ES_f = open('ES_data.json', 'r')
ES = json.load(ES_f)

ESE5_f = open('ESE5_data.json', 'r')
ESE5 = json.load(ESE5_f)

ESE6_f = open('ESE6_data.json', 'r')
ESE6 = json.load(ESE6_f)

ESE7_f = open('ESE7_data.json', 'r')
ESE7 = json.load(ESE7_f)

X1_f = open('X1_data.json', 'r')
X1 = json.load(X1_f)

DS_f = open('DS_data.json', 'r')
DS = json.load(DS_f)

HS_f = open('HS_data.json', 'r')
HS = json.load(HS_f)

HSH1_f = open('HSH1_data.json', 'r')
HSH1 = json.load(HSH1_f)

HSH2_f = open('HSH2_data.json', 'r')
HSH2 = json.load(HSH2_f)

HSH3_f = open('HSH3_data.json', 'r')
HSH3 = json.load(HSH3_f)

HSH4_f = open('HSH4_data.json', 'r')
HSH4 = json.load(HSH4_f)

HSH5_f = open('HSH5_data.json', 'r')
HSH5 = json.load(HSH5_f)

HSH6_f = open('HSH6_data.json', 'r')
HSH6 = json.load(HSH6_f)

X3_f = open('X3_data.json', 'r')
X3 = json.load(X3_f)

GF_f = open('GF_data.json', 'r')
GF = json.load(GF_f)

GH_f = open('GH_data.json', 'r')
GH = json.load(GH_f)

print("> シラバスデータ取得完了")
print("\n")


gakubu = CS

for i in range(0, len(gakubu)):
    if serchIndexCheck(gakubu[i][4], args[1]):
        print("時間割コード： " + args[1])
        print(gakubu[i][0] + " の" + "単位数は " + gakubu[i][9] + " です")
 """
