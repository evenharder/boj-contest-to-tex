# boj-contest-to-tex
 BOJ 대회 결과를 편리하게 LaTeX 파일로 가공하는 스크립트 모음

# 범례
- `boj_contest_to_tex.py`, Python 3.7+
  - [Beautiful Soup 4](https://pypi.org/project/beautifulsoup4/) 패키지가 필요합니다.
  - `class SpotboardAnalyzer` : Spotboard의 `contest.json`과 `runs.json`을 받아 LaTeX pgfplots와 호환되는 시간별 제출 횟수 데이터를 생성합니다.
  - `class BOJStatisticsAnalyzer` : BOJ 대회의 '통계' 페이지를 분석해 일반적으로 해설지 문제별 첫 슬라이드에 들어가는 정보를 LaTeX 형식으로 생성합니다.
- `icpcbar.sty` : `SpotboardAnalyzer`로 생성된 데이터를 LaTeX pgfplots를 이용한 stacked bar chart로 시각화하는 패키지입니다.
  - 색상은 [Paul Tol의 색상표](https://personal.sron.nl/~pault/#sec:qualitative)를 이용했습니다.
  - 사용 예시 : [UCPC 2023 예선 해설지](https://static.ucpc.me/files/2023/ucpc23-prelim-solutions.pdf)
  
다음은 테스트용 파일입니다.
- `bct_test.py`, Python 3.7+
  - [Requests](https://pypi.org/project/requests/) 패키지가 필요합니다.
  - 실행하면 [UCPC 2021 본선](https://www.acmicpc.net/contest/view/670)의 데이터를 분석합니다.

# 주의 사항
- `BOJStatisticsAnalyzer`는 현재 BOJ 팀 대회만 지원합니다.
- `icpcbar.sty`는 대회 시간이 60등분 되었을 때 이상적으로 작동하며, 그 외 간격에서는 그래프가 겹치거나 간격이 생길 수 있습니다.