import json
import tempfile
import requests
from boj_contest_to_tex import SpotboardAnalyzer, BOJStatisticsAnalyzer

print('boj_contest_to_tex: UCPC 2021 Finals')

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}

def get_resp(url):
    resp = requests.get(url, headers=headers)
    print(f'GET {url} {resp.status_code}')
    if not resp.ok:
        exit(1)
    return resp

resp_st = get_resp(
'https://www.acmicpc.net/contest/statistics/670')
resp_contest = get_resp(
'https://www.acmicpc.net/contest/spotboard/670/contest.json')
resp_runs = get_resp(
'https://www.acmicpc.net/contest/spotboard/670/runs.json')

temp_path = tempfile.mkdtemp()
temp_gen_path = f'{temp_path}/ucpc2021-final'

boj_st_analyzer = BOJStatisticsAnalyzer(resp_st.text)
boj_st_analyzer.print_beamer_style()

sb_analyzer = SpotboardAnalyzer(json.loads(
resp_contest.text), json.loads(resp_runs.text))
sb_analyzer.export_full_data(temp_gen_path,
                         interval=5, is_frozen=True)
print(f'SpotboardAnalyzer data generated in {temp_path}')
