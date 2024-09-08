import ssl
from typing import Any
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

def _text_fotmat(text: str) -> str:
    return text.strip().replace(' ', '').replace(
        '\r\n', '').replace('\u30001', '').replace('\u3000', '').replace('\n', '').replace('\r', '').replace('\t', '')


def _join_lecture_information(lecture_informations: ResultSet[Any]) -> list[str]:
    joined_lecture_information_list = []

    for lecture_information in lecture_informations:
        td_data = lecture_information.find_all('td')

        for td in td_data:
            joined_lecture_information_list.append(_text_fotmat(td.text))

    return joined_lecture_information_list

# ===========================================================================
# 講義データ取得関数 (時間割コード => 授業内容等(単位数))
# ===========================================================================
def get_timetable(department_name: str, lecture_code : str,):
    now_year = datetime.datetime.now().year
    res = _fetch_syllabus(now_year, department_name, lecture_code)

    if res.status_code == 404:
        return None

    bs = BeautifulSoup(res.content, 'html.parser')

    tab_elements = bs.find_all('table', class_='syllabus-normal')

    # 講義情報を格納するリスト
    joined_lists = _join_lecture_information(tab_elements)

    print(joined_lists)


get_timetable('CS','11041C1')
