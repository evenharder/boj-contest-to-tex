#!/usr/bin/env python3
import tempfile
import requests
import json
from boj_contest_to_tex import SpotboardAnalyzer, BOJStatisticsAnalyzer

print("boj_contest_to_tex: UCPC 2023 Finals")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}


def get_resp(url):
    resp = requests.get(url, headers=headers)
    print(f"GET {url} {resp.status_code}")
    if not resp.ok:
        exit(1)
    return resp


def test_spotboard_analyzer(idx):
    resp_contest = get_resp(
        f"https://www.acmicpc.net/contest/spotboard/{idx}/contest.json"
    )
    resp_runs = get_resp(f"https://www.acmicpc.net/contest/spotboard/{idx}/runs.json")

    temp_path = tempfile.mkdtemp()
    temp_gen_path = f"{temp_path}/ucpc2023-final"

    # uncomment this if you want to work offline (e.g. private competition)
    """
    with open("./ucpc2023-json/contest.json") as f:
        resp_contest = json.load(f)
    with open("./ucpc2023-json/runs.json") as f:
        resp_runs = json.load(f)
    sb_analyzer = SpotboardAnalyzer(resp_contest, resp_runs)
    """

    sb_analyzer = SpotboardAnalyzer(
        json.loads(resp_contest.text), json.loads(resp_runs.text)
    )
    sb_analyzer.export_full_data(temp_gen_path, interval=5, is_frozen=True)

    print(f"SpotboardAnalyzer data generated in {temp_path}")


def test_boj_analyzer(idx):
    resp_st = get_resp(f"https://www.acmicpc.net/contest/statistics/{idx}")
    boj_st_analyzer = BOJStatisticsAnalyzer(resp_st.text)
    boj_st_analyzer.print_beamer_style()


def test_component(msg, func):
    print(f"{msg} started\n")
    func()
    print(f"{msg} finished\n")


def test_idx(idx):
    test_component("SpotboardAnalyzer", lambda: test_spotboard_analyzer(idx))
    test_component("BOJStatisticsAnalyzer", lambda: test_boj_analyzer(idx))


test_idx(828)  # UCPC 2022 Final
test_idx(1069)  # UCPC 2023 Final
