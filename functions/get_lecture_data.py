from bs4 import BeautifulSoup
import requests
import re
import datetime

# ===========================================================================
# 講義データ取得関数 (時間割コード => 授業内容等(単位数))
# ===========================================================================

class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

def fetch_syllabus(url: str):
    session = requests.session()
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4
    session.mount('https://', CustomHttpAdapter(ctx))
    res = session.get(url)
    return res

def get_timetable(lecture_code : str, department_name : str):
    now_year = datetime.datetime.now().year
    print("...取得中")
        print(val)

    res = fetch_syllabus(f'https://kyo-web.teu.ac.jp/syllabus/{now_year}/{department_name}_{lecture_code}_ja_JP.html')

    if res.status_code == 404:
        continue
    bs = BeautifulSoup(res.content, 'html.parser')
    table_elements = bs.find_all('table', class_='syllabus-normal')[0]
    tds = table_elements.find_all('td')

    ary = {}

    for td in tds:
        ary.append(td.get_text().strip().replace(' ', '').replace(
            '\r\n', '').replace('\u30001', '').replace('\u3000', ''))


