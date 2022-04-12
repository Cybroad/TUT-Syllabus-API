# ====================================================
# 東京工科大学 学内シラバス 科目情報取得ツール
#
# 開発元：TUT22 Dev Team (tut22_dev@6mile.dev)
# ====================================================
import getTimeTable
import getData
department = 18
for i in range(department):
    print()
    x = getTimeTable.getcode(i)
    if x == "finish":
        getData.get_timetable(i)
"""def Bt():
    Select(driver.find_element_by_id(
        'jikanwariShozokuCode')).select_by_value('﻿BT')


def Cs():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('CS')  # コンピュータサイエンス学部


def Ms():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('MS')  # メディア学部


def Es():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('ES')  # 工学部


def Ese5():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('ESE5')  # 機械工学科


def Ese6():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('ESE6')  # 電気電子工学科


def Ese7():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('ESE7')  # 応用科学科


def x1():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('X1')  # 教養教育科目(八王子同会議)


def Ds():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('DS')  # デザイン学部


def Hs():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('HS')  # 医療保健学部


def Hsh1():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('HSH1')  # 看護学科


def Hsh2():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('HSH2')  # 臨床工学科


def Hsh3():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('HSH3')  # 理学医療学科


def Hsh4():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('HSH4')  # 作業療法学科


def Hsh5():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('HSH5')  # 臨床検査学科


def Hsh6():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('HSH6')  # リハビリテーション学科


def x3():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('X3')  # 大学院


def Gf():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('GF')  # デザイン研究科


def Gh():
    Select(driver.find_element_by_id('jikanwariShozokuCode')
           ).select_by_value('GH')  # 医療技術学研究科"""
