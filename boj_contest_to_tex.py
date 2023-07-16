from bs4 import BeautifulSoup


class BOJContestProblem:
    def __init__(self):
        self._is_frozen = False
        self._id = None
        self._name = None
        self._ac_num = None
        self._ac_ratio = None
        self._total_sub = None
        self._fs_time = None
        self._fs_teamname = None
        self._fs_members = None
        self._author = None

    @property
    def is_frozen(self):
        return self._is_frozen

    @is_frozen.setter
    def is_frozen(self, val):
        self._is_frozen = val

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def ac_num(self):
        if self._is_frozen:
            return str(self._ac_num) + ' + ?'
        return int(self._ac_num)

    @ac_num.setter
    def ac_num(self, val):
        self._ac_num = int(val)

    @property
    def ac_ratio(self):
        if self._is_frozen:
            return str(f'??.???\%')
        elif self._ac_num:
            return self._ac_ratio
        else:
            return f'-\%'

    @ac_ratio.setter
    def ac_ratio(self, val):
        self._ac_ratio = str(val).replace('%', f'\%')

    @property
    def total_sub(self):
        if self._is_frozen:
            return str(self._total_sub) + ' + ?'
        return self._total_sub

    @total_sub.setter
    def total_sub(self, val):
        self._total_sub = int(val)

    @property
    def fs_time(self):
        if self._fs_time is None:
            if self._is_frozen:
                return '???'
            else:
                return '--'
        return self._fs_time

    @fs_time.setter
    def fs_time(self, val):
        self._fs_time = int(''.join([x for x in str(val) if x.isdigit()]))

    @property
    def fs_teamname(self):
        if self._fs_teamname is None:
            if self._is_frozen:
                return '???'
            else:
                return '--'
        return self._fs_teamname

    @fs_teamname.setter
    def fs_teamname(self, val):
        self._fs_teamname = val

    @property
    def fs_members(self):
        if self._fs_members is None:
            if self._is_frozen:
                return '(?, ?, ?)'
            else:
                return '-, -, -'
        return self._fs_members

    @fs_members.setter
    def fs_members(self, val):
        self._fs_members = val

    @property
    def fs_data(self):
        if self._fs_teamname is None and self._is_frozen is False:
            return '--'
        return rf'\textbf{{{self.fs_teamname}}} {self.fs_members}, {self.fs_time}분'

    @property
    def fs_data_short(self):
        if self._fs_teamname is None and self._is_frozen is False:
            return '--'
        return rf'\textbf{{{self.fs_teamname}}}, {self.fs_time}분'

    @property
    def author(self):
        if self._author is None:
            return 'placeholder'
        return self._author

    @author.setter
    def author(self, val):
        self._author = val

    def __repr__(self):
        return f'''{self.id} - {self.name}
{self.ac_num}/{self.total_sub} ({self.ac_ratio})
First solve : {self.fs_teamname}, {self.fs_members}, {self.fs_time}'''

    def split_teamname(self, s):
        team_par_index = s.index('(')  # looks like spotboard sanitize () to ❨❩
        self.fs_teamname = s[:team_par_index].strip()
        self.fs_members = s[team_par_index:].strip()

    def beamer_str(self, *, indent=' ' * 4):
        return rf'''{indent}% {self.id} - {self.name}
{indent}\begin{{itemize}}
{indent}{indent}\item 제출 {self.total_sub}번, 정답 {self.ac_num}팀 (정답률 {self.ac_ratio})
{indent}{indent}\item 처음 푼 팀: {self.fs_data}
{indent}{indent}\item 출제자: \texttt{{{self.author}}}
{indent}\end{{itemize}}
'''


class SpotboardAnalyzer:
    '''
    A data structure handling Spotboard json data.
    '''

    def __init__(self, contest_json, runs_json):
        '''
        Constructor.

        contest_json
          dict from Spotboard 'contest.json'.
        runs_json
          dict from Spotboard 'runs_json'.
        '''
        self.contest_json = contest_json
        self.runs_json = runs_json
        self.problems = contest_json['problems']
        self.teams = contest_json['teams']
        self.team_ac = {team['id']: set() for team in self.teams}

    def generate_run_data(self, *, problem_list=None, interval=5, contest_time=None, is_frozen=False):
        '''
        Return run data as a list where the first item includes labels,
        and the others contain timeframe and the number of each verdict
        (yes, no, pending).

        Generated run data, if printed, is compatible with
        LaTex pgfplots datatable format.

        Figures of No verdict are negated to display No submissions as
        negative stacked bar in LaTeX.

        problem_list
          list of desired spotboard problem ids, defaults to all problems.
        interval
          interval between timeframes starting from 0min, defaults to 5
        contest_time.
          total contest time for data,
          defaults to whole contest time based on contest_json.
        is_frozen
          whether to display frozen subs as frozen, default to False.
        '''
        if problem_list is None:
            problem_list = [problem['id'] for problem in self.problems]
        if contest_time is None:
            contest_time = self.runs_json['time']['contestTime'] // 60
        team_ac = {team['id']: set() for team in self.teams}

        run_data = [['Interval', 'Yes', 'No', 'Pending']]
        for t in range(0, contest_time + 1, interval):
            run_data.append([t, 0, 0, 0])
        runs = self.runs_json['runs']
        for cur_run in runs:
            if cur_run['problem'] not in problem_list:
                continue
            if cur_run['problem'] in team_ac[cur_run['team']]:
                continue
            tid = cur_run['submissionTime'] // interval + 1
            if cur_run['frozen'] and is_frozen:
                run_data[tid][3] += 1
            elif cur_run['result'] == 'Yes':
                run_data[tid][1] += 1
                team_ac[cur_run['team']].add(cur_run['problem'])
            else:
                run_data[tid][2] -= 1
        for i in range(len(run_data)):
            run_data[i] = [str(x) for x in run_data[i]]
        return run_data

    def generate_problem_data(self, prob_id, is_frozen=True):
        contest_prob = BOJContestProblem()
        contest_prob.id = self.problems[prob_id]['name']
        contest_prob.name = self.problems[prob_id]['title']
        contest_prob.total_sub = 0
        contest_prob.ac_num = 0

        team_ac = {team['id']: set() for team in self.teams}

        runs = self.runs_json['runs']
        is_first = False
        for cur_run in runs:
            if cur_run['problem'] != prob_id:
                continue
            if is_frozen and cur_run['frozen']:
                continue
            contest_prob.total_sub += 1
            if cur_run['problem'] in self.team_ac[cur_run['team']]:
                continue
            if cur_run['result'] == 'Yes':
                self.team_ac[cur_run['team']].add(cur_run['problem'])
                contest_prob.ac_num += 1
                if is_first is False:
                    contest_prob.fs_time = cur_run['submissionTime']
                    team_id = cur_run['team']
                    fs_team = list(
                        filter(lambda x: x['id'] == team_id, self.teams))[0]
                    contest_prob.split_teamname(fs_team['name'])
                    is_first = True

        contest_prob.is_frozen = is_frozen
        print(contest_prob.beamer_str())
        return contest_prob

    def export_run_data(self, run_data, path):
        '''
        Export run data to a file.

        run_data:
          a list generated by generate_run_data.
        path:
          path to export file
        '''
        with open(path, 'w') as f:
            for line in run_data:
                f.write('\t'.join(line))
                f.write('\n')

    def print_run_data(self, run_data):
        '''
        Print run data to stdout.

        run_data
          a list generated by generate_run_data.
        '''
        for line in run_data:
            print('\t'.join(line))

    def export_full_data(self, filename_prefix, **kwargs):
        '''
        Generate and export run data for all submissions regardless of problem id,
        as well as run data for each problem.

        filename_prefix
          path prefix for generated files.
        **kwargs
          keyword arguments directly passed to generate_run_data.
        '''
        problem_lists = []
        for problem in self.problems:
            problem_lists.append([problem['id']])
        problem_lists.append([problem['id'] for problem in self.problems])

        filenames = []
        for problem in self.problems:
            filenames.append(f'{filename_prefix}-{problem["name"]}.txt')
        filenames.append(f'{filename_prefix}-@.txt')

        for problem_list, filename in zip(problem_lists, filenames):
            self.export_run_data(self.generate_run_data(
                problem_list=problem_list, **kwargs), filename)
            problem_id = problem_list[0]
            self.generate_problem_data(problem_id)


class BOJStatisticsAnalyzer:
    '''
    A data structure which easily converts BOJ Statistics to LaTeX format,
    especially aligned with UCPC editorial.
    '''

    def __init__(self, html_page):
        '''
        Constructor.

        Support only BOJ team contest page as of now.

        html_page
          str object indicating html of BOJ Contest statistics page.
        '''
        soup = BeautifulSoup(html_page, 'html.parser')
        arr = soup.get_text(separator='\n', strip=True).split('\n')

        def index_r(arr, start, *args):
            ind = start
            for arg in args:
                if ind == -1:
                    return -1
                ind = arr.index(arg, start) + 1
            return ind if ind < len(arr) else -1

        contest_title = arr[0][:-5].strip()
        prob_nums = (index_r(arr, 1, contest_title, '합계') -
                     index_r(arr, 1, contest_title, '문제 통계') - 1)
        self.boj_probs = [BOJContestProblem() for _ in range(prob_nums)]
        prob_index = index_r(arr, 1, contest_title, '질문')
        for i in range(prob_nums):
            j = prob_index + 2 * i
            self.boj_probs[i].id = arr[j].strip()
            self.boj_probs[i].name = arr[j + 1][1:].strip()
        ac_index = index_r(arr, prob_index, '맞은 사람')
        for i in range(prob_nums):
            j = ac_index + i
            self.boj_probs[i].ac_num = arr[j].strip()
        ac_ratio_index = index_r(arr, ac_index, '정답율')
        for i in range(prob_nums):
            j = ac_ratio_index + i
            self.boj_probs[i].ac_ratio = arr[j].strip()
        total_sub_index = index_r(arr, ac_index, '총 제출')
        for i in range(prob_nums):
            j = total_sub_index + i
            self.boj_probs[i].total_sub = arr[j].strip()
        fs_index = index_r(arr, total_sub_index, '맞았습니다')
        prob_index = 0
        while True:
            if arr[fs_index].find('-') == -1:
                break
            bar_index = arr[fs_index].find('-')
            cur_id = arr[fs_index][:bar_index - 1].strip()
            cur_name = arr[fs_index][bar_index + 1:].strip()
            while prob_index < len(self.boj_probs) and \
                self.boj_probs[prob_index].id != cur_id or \
                    self.boj_probs[prob_index].name != cur_name:
                prob_index += 1
            if prob_index == len(self.boj_probs):
                break
            cur_prob = self.boj_probs[prob_index]
            cur_prob.split_teamname(arr[fs_index + 2])
            cur_prob.fs_time = arr[fs_index + 3][1:].strip()
            fs_index += 4

    def print_beamer_style(self, *, tab_size=4, is_space=True, fd=None):
        '''
        print parsed and analyzed statistics page in UCPC beamer editorial format.

        tab_size
          number of space for indentation, defaults to 4.
        is_space
          whether to use space of tab, defaults to True (space).
        fd
          a file-like object (stream) passed to print,
          defaults to current sys.stdout.
        '''
        def ratio_conv(ratio):
            return ratio[:-1] + '\%'
        for boj_prob in self.boj_probs:
            indent = ' ' * tab_size if is_space else '\t'
            print(boj_prob.beamer_str(indent=indent), file=fd)


if __name__ == '__main__':
    pass
