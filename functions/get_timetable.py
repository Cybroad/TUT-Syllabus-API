from lxml import html
import ssl
from bs4 import BeautifulSoup, ResultSet
import requests
import datetime
import urllib3

TUT_SYLLABUS_URL = 'https://kyo-web.teu.ac.jp/syllabus'

class _CustomHttpAdapter (requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

def _fetch_syllabus(current_year: int, department_name: str, lecture_code: str):
    session = requests.session()
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4
    session.mount('https://', _CustomHttpAdapter(ctx))
    res = session.get(f'{TUT_SYLLABUS_URL}/{current_year}/{department_name}_{lecture_code}_ja_JP.html')
    return res

def _format_string(text: str) -> str:
    return text.strip().replace(' ', '').replace(
    '\r\n', '').replace('\u30001', '').replace('\u3000', '').replace('\n', '').replace('\r', '').replace('\t', '').replace(u'\xa0', u'')


def _format_lecture_information(lecture_information: ResultSet) -> list[str]:
    td_data = lecture_information.find_all('td')
    return [_format_string(td.text) for td in td_data if td]

def _exsistCheck(targetLst: list, index: int) -> bool:
    try:
        targetLst[index]
        return True
    except IndexError:
        return False


# ===========================================================================
# 講義データ取得関数 (時間割コード => 授業内容等(単位数))
# ===========================================================================
def get_timetable(department_name: str, lecture_code : str) -> dict:
    now_year = datetime.datetime.now().year
    res = _fetch_syllabus(now_year, department_name, lecture_code)

    if res.status_code == 404:
        return None

    bs = BeautifulSoup(res.content, 'html.parser')

    # 講義情報が存在しない場合
    if not bs.find_all('table', class_='syllabus-normal'):
        return None
    
    # 最終更新日時を取得
    lxml_data = html.fromstring(str(bs))
    update_at = lxml_data.xpath('/html/body/table')[1]
    update_at_text = _format_string(update_at.text_content().replace('閉じる', '').replace('現在', ''))

    # 表を区別するタブ1, タブ2の要素を取得
    tab1_elements = bs.find_all('table', class_='syllabus-normal')[0]
    tab2_elements = bs.find_all('table', class_='syllabus-normal')[1]

    # 講義情報を取得
    tab1_data = _format_lecture_information(tab1_elements)
    tab2_data = _format_lecture_information(tab2_elements)

    # dictに変換
    lecture_data = {
        'lectureCode': lecture_code,
        'courseName': tab1_data[0] if _exsistCheck(tab1_data, 0) else '',
        'lecturer': tab1_data[1].split(',') if _exsistCheck(tab1_data, 1) else [],
        'regularOrIntensive': tab1_data[2] if _exsistCheck(tab1_data, 2) else '',
        'courseType': tab1_data[3] if _exsistCheck(tab1_data, 3) else '',
        'courseStart': tab1_data[5] if _exsistCheck(tab1_data, 5) else '',
        'classPeriod': tab1_data[6].split(',') if _exsistCheck(tab1_data, 6) else [],
        'targetDepartment': tab1_data[7] if _exsistCheck(tab1_data, 7) else '',
        'targetGrade': tab1_data[8].split(',') if _exsistCheck(tab1_data, 8) else [],
        'numberOfCredits': int(float(tab1_data[9])) if _exsistCheck(tab1_data, 9) else 0,
        'classroom': tab1_data[10].split(',') if _exsistCheck(tab1_data, 10) else [],
        'courceDetails': {
            'courseOverview': tab2_data[1] if _exsistCheck(tab2_data, 1) else '',
            'outcomesMeasuredBy': tab2_data[2] if _exsistCheck(tab2_data, 2) else '',
            'learningOutcomes': tab2_data[3] if _exsistCheck(tab2_data, 3) else '',
            'teachingMethod': tab2_data[4] if _exsistCheck(tab2_data, 4) else '',
            'notices': tab2_data[5] if _exsistCheck(tab2_data, 5) else '',
            'preparatoryStudy': tab2_data[6] if _exsistCheck(tab2_data, 6) else '',
            'gradingGuidelines': tab2_data[7] if _exsistCheck(tab2_data, 7) else '',
            'textbook': tab2_data[8] if _exsistCheck(tab2_data, 8) else '',
            'referenceMaterials': tab2_data[9] if _exsistCheck(tab2_data, 9) else '',
            'courseSchedule': tab2_data[10] if _exsistCheck(tab2_data, 10) else '',
            'courseDataUpdatedAt': tab2_data[0] if _exsistCheck(tab2_data, 0) else ''
        },
        'updateAt': update_at_text
    }

    return lecture_data
