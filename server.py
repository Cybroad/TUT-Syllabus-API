from fastapi import FastAPI
import json

# =============================================================================
# 各学部毎の配列作成
# =============================================================================

BT = open('BT_data.json', 'r')
BT_d = json.load(BT)

CS = open('CS_data.json', 'r')
CS_d = json.load(CS)

MS = open('MS_data.json', 'r')
MS_d = json.load(MS)

ES = open('ES_data.json', 'r')
ES_d = json.load(ES)

ESE5 = open('ESE5_data.json', 'r')
ESE5_d = json.load(ESE5)

ESE6 = open('ESE6_data.json', 'r')
ESE6_d = json.load(ESE6)

ESE7 = open('ESE7_data.json', 'r')
ESE7_d = json.load(ESE7)

X1 = open('X1_data.json', 'r')
X1_d = json.load(X1)

DS = open('DS_data.json', 'r')
DS_d = json.load(DS)

HS = open('HS_data.json', 'r')
HS_d = json.load(HS)

HSH1 = open('HSH1_data.json', 'r')
HSH1_d = json.load(HSH1)

HSH2 = open('HSH2_data.json', 'r')
HSH2_d = json.load(HSH2)

HSH3 = open('HSH3_data.json', 'r')
HSH3_d = json.load(HSH3)

HSH4 = open('HSH4_data.json', 'r')
HSH4_d = json.load(HSH4)

HSH5 = open('HSH5_data.json', 'r')
HSH5_d = json.load(HSH5)

HSH6 = open('HSH6_data.json', 'r')
HSH6_d = json.load(HSH6)

X3 = open('X3_data.json', 'r')
X3_d = json.load(X3)

GF = open('GF_data.json', 'r')
GF_d = json.load(GF)

GH = open('GH_data.json', 'r')
GH_d = json.load(GH)

# =============================================================================


app = FastAPI()


@ app.get("/")
def read_root():
    return "Hello World"


@ app.get("/getInfo/{department}/{id}")
def getTimeTableInfo(department: str, id: str):
    if department == "BT":
        return BT_d[int(id)]
