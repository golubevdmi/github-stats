from __future__ import print_function

import github
import argparse
import sys
from datetime import timedelta, datetime
import calendar
import csv
from copy import deepcopy
from itertools import tee

# For OpenCV
import numpy as np
import cv2

# For Google Drive API
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload


class PullRequests:
    def __sub__(self, other):
        out = PullRequests()

        out.all = self.all - other.all
        out.open = self.open - other.open
        out.opened = self.opened - other.opened
        out.closed = self.closed - other.closed
        out.merged = self.merged - other.merged

        return out

    def get_stat(self, repo, date_begin, date_end):
        self.all = 0
        self.open = 0
        self.opened = 0
        self.closed = 0
        self.merged = 0

        for pr in repo.get_pulls(state='all', sort='created_at'):
            assert (pr.created_at is not None)

            counter_inc = False

            if pr.created_at.date() > date_end:
                break

            if (pr.created_at.date() < date_begin) and \
                    ((pr.closed_at is None or pr.closed_at.date() > date_begin) and
                     (pr.merged_at is None or pr.merged_at.date() > date_begin)):
                self.open += 1
                counter_inc = True

            if date_begin <= pr.created_at.date() <= date_end:
                self.opened += 1
                counter_inc = True

            if pr.merged_at is not None and \
                    date_begin <= pr.merged_at.date() <= date_end:
                self.merged += 1
                counter_inc = True

            if pr.closed_at is not None and \
                    date_begin <= pr.closed_at.date() <= date_end:
                self.closed += 1
                counter_inc = True

            if counter_inc is True:
                self.all += 1

    def copy(self):
        out = PullRequests()

        out.all = deepcopy(self.all)
        out.open = deepcopy(self.open)
        out.opened = deepcopy(self.opened)
        out.closed = deepcopy(self.closed)
        out.merged = deepcopy(self.merged)

        return out

    def show(self):
        print('\tPullR: ',
              '\tall:', self.all,
              '\topen:', self.open,
              '\topened:', self.opened,
              '\tclosed:', self.closed,
              '\tmerged:', self.merged)

    all: int = 0
    open: int = 0
    opened: int = 0
    closed: int = 0
    merged: int = 0


class Issues:
    def __sub__(self, other):
        out = Issues()

        out.all = self.all - other.all
        out.open = self.open - other.open
        out.opened = self.opened - other.opened
        out.closed = self.closed - other.closed

        return out

    def get_stat(self, repo, date_begin, date_end):
        self.all = 0
        self.open = 0
        self.opened = 0
        self.closed = 0

        for issue in reversed(list(repo.get_issues(state='all'))):
            assert (issue.created_at is not None)
            counter_inc = False

            if issue.created_at.date() > date_end:
                break

            if (issue.created_at.date() < date_begin) and \
                    (issue.closed_at is None or issue.closed_at.date() > date_begin):
                self.open += 1
                counter_inc = True

            if date_begin <= issue.created_at.date() <= date_end:
                self.opened += 1
                counter_inc = True

            if issue.closed_at is not None and \
                    date_begin <= issue.closed_at.date() <= date_end:
                self.closed += 1
                counter_inc = True

            if counter_inc is True:
                self.all += 1

    def copy(self):
        out = Issues()

        out.all = deepcopy(self.all)
        out.open = deepcopy(self.open)
        out.opened = deepcopy(self.opened)
        out.closed = deepcopy(self.closed)

        return out

    def show(self):
        print('\tIssues: ',
              '\tall:', self.all,
              '\topen:', self.open,
              '\topened:', self.opened,
              '\tclosed:', self.closed)

    all: int = 0
    open: int = 0
    opened: int = 0
    closed: int = 0


class Stars:
    def __sub__(self, other):
        out = Stars()

        out.all = self.all - other.all
        out.snapshot = self.snapshot - other.snapshot
        out.period = self.period - other.period

        return out

    def get_stat(self, repo, date_begin, date_end):
        self.all = 0
        self.snapshot = 0
        self.period = 0

        for star in repo.get_stargazers_with_dates():
            assert (star.starred_at is not None)

            counter_inc = False

            if star.starred_at.date() > date_end:
                break

            if date_begin <= star.starred_at.date() <= date_end:
                self.period += 1
                counter_inc = True

            if star.starred_at.date() <= date_begin:
                self.snapshot += 1
                counter_inc = True

            if counter_inc is True:
                self.all += 1

    def copy(self):
        out = Stars()

        out.all = deepcopy(self.all)
        out.snapshot = deepcopy(self.snapshot)
        out.period = deepcopy(self.period)

        return out

    def show(self):
        print('\tStars:',
              '\t\tall:', self.all,
              '\tStars snapshot:', self.snapshot,
              '\tStars per period:', self.period)

    all: int = 0
    snapshot: int = 0
    period: int = 0


class Forks:
    def __sub__(self, other):
        out = Forks()

        out.all = self.all - other.all
        out.snapshot = self.snapshot - other.snapshot
        out.period = self.period - other.period

        return out

    def get_stat(self, repo, date_begin, date_end):
        self.all = 0
        self.snapshot = 0
        self.period = 0

        for fork in reversed(list(repo.get_forks())):
            assert (fork.created_at is not None)
            counter_inc = False

            if fork.created_at.date() > date_end:
                break

            if fork.created_at.date() <= date_begin:
                self.snapshot += 1
                counter_inc = True

            if date_begin <= fork.created_at.date() <= date_end:
                self.period += 1
                counter_inc = True

            if counter_inc is True:
                self.all += 1

    def copy(self):
        out = Forks()

        out.all = deepcopy(self.all)
        out.snapshot = deepcopy(self.snapshot)
        out.period = deepcopy(self.period)

        return out

    def show(self):
        print('\tForks:',
              '\t\tall:', self.all,
              '\tForks snapshot:', self.snapshot,
              '\tForks per period:', self.period)

    all: int = 0
    snapshot: int = 0
    period: int = 0


class Traffic:
    def __sub__(self, other):
        out = Traffic()

        out.visitors = self.visitors - other.visitors
        out.cloners = self.cloners - other.cloners

        return out

    # --TODO error Message 403
    def get_stat(self, repo, date_begin, date_end):
        self.visitors = 0
        self.cloners = 0

        try:
            self.visitors = repo.get_views_traffic(per='week')['uniques']
            self.cloners = repo.get_clones_traffic(per='week')['uniques']
        except Exception as exc:
            self.visitors = -1
            self.cloners = -1

    def copy(self):
        out = Traffic()

        out.visitors = deepcopy(self.visitors)
        out.cloners = deepcopy(self.cloners)

        return out

    def show(self):
        print('\tTraffic:',
              '\tVisitors unique:', self.visitors,
              '\tCloners unique:', self.cloners)

    visitors: int = 0
    cloners: int = 0


class GithubStats:
    def __init__(self, begin=str(), end=str()):
        self.begin = begin
        self.end = end

    def __sub__(self, other):
        out = GithubStats()

        out.pulls = self.pulls - other.pulls
        out.issues = self.issues - other.issues
        out.stars = self.stars - other.stars
        out.forks = self.forks - other.forks
        out.traffic = self.traffic - other.traffic

        return out

    def get_stat(self, repo, period1, period2):
        self.begin = datetime.strftime(period1, '%Y.%m.%d')
        self.end = datetime.strftime(period2, '%Y.%m.%d')

        self.pulls.get_stat(repo, period1, period2)
        self.issues.get_stat(repo, period1, period2)
        self.stars.get_stat(repo, period1, period2)
        self.forks.get_stat(repo, period1, period2)
        self.traffic.get_stat(repo, period1, period2)

    def copy(self):
        out = GithubStats()
        out.begin = deepcopy(self.begin)
        out.end = deepcopy(self.end)
        out.tag = deepcopy(self.tag)

        out.pulls = self.pulls.copy()
        out.issues = self.issues.copy()
        out.stars = self.stars.copy()
        out.forks = self.forks.copy()
        out.traffic = self.traffic.copy()

        return out

    def show(self):
        print('\nPeriod:', self.begin, self.end,
              '\nTag:', self.tag)

        self.pulls.show()
        self.issues.show()
        self.stars.show()
        self.forks.show()
        self.traffic.show()

    begin = str()
    end = str()
    tag = str()

    pulls = PullRequests()
    issues = Issues()
    stars = Stars()
    forks = Forks()
    traffic = Traffic()


def show_metric_snapshot(repo):
    print('Metric snapshot:',
          '\n\tPR open:', repo.open_pulls_count,
          '\n\tIssues open:', repo.open_issues_count,
          '\n\tStars:', repo.stargazers_count,
          '\n\tForks:', repo.forks_count, )


def write_opencv(file_name, stats_array):
    print('Save to', file_name)

    # Open OpenCV file storage
    fs = cv2.FileStorage(file_name, cv2.FileStorage_WRITE)

    if fs.isOpened() is False:
        sys.exit('File is not open')

    matrix = []
    for stats in stats_array:
        fs.write('Period stats', str(stats.begin + ' - ' + stats.end))
        fs.write('Tag', stats.tag)

        # Save pulls data to file
        fs.write('PR open', stats.pulls.open)
        fs.write('PR opened', stats.pulls.opened)
        fs.write('PR closed', stats.pulls.closed)
        fs.write('PR merged', stats.pulls.merged)

        # Save issues data to file
        fs.write('Issues open', stats.issues.open)
        fs.write('Issues opened', stats.issues.opened)
        fs.write('Issues closed', stats.issues.closed)

        # Save stars data to file\
        fs.write('Stars snapshot', stats.stars.snapshot)
        fs.write('Stars per period', stats.stars.period)

        # Save forks data to file
        fs.write('Forks snapshot', stats.forks.snapshot)
        fs.write('Forks per period', stats.forks.period)

        fs.write('Visitors uniques', stats.traffic.visitors)
        fs.write('Cloners uniques', stats.traffic.cloners)

        # Create stats array
        arr = np.array([stats.pulls.open, stats.issues.open, stats.stars.snapshot, stats.forks.snapshot,
                        stats.traffic.visitors, stats.traffic.cloners, stats.pulls.opened, stats.pulls.merged,
                        stats.pulls.closed,
                        stats.issues.opened, stats.issues.closed, stats.forks.period])
        matrix.append(arr)

        fs.write('stat_array', arr)

    fs.write('output_matrix', np.asmatrix(matrix))
    fs.release()


def write_csv(file_name, stats_array):
    print('Save to', file_name)
    writer = csv.writer(open(file_name, 'w', newline=''), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Period', 'PR open', 'Issue open', 'Stars snapshot', 'Forks snapshot',
                     'Visitors (uniques)', 'Cloners (uniques)', 'PR opened', 'PR merged', 'PR closed',
                     'Issues opened', 'Issues closed', 'Stars per period', 'Forks per period'])
    for stats in stats_array:
        writer.writerow([stats.begin + ' - ' + stats.end + ' ' + stats.tag,
                         stats.pulls.open, stats.issues.open,
                         stats.stars.snapshot, stats.forks.snapshot, stats.traffic.visitors, stats.traffic.cloners,
                         stats.pulls.opened, stats.pulls.merged, stats.pulls.closed,
                         stats.issues.opened, stats.issues.closed, stats.stars.period, stats.forks.period])


def write_gdocs(file_name, stats_array):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    try:
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_name,
                                mimetype='application/octet-stream',
                                resumable=True)
        file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
        print('File ID: %s' % file.get('id'))
    except Exception as exc:
        print(exc)


# Parsing periods by tags or dates
# If tags are defined, returned True
# Return check tags, parsed periods
def parsing_period(repo, periods):
    isTags = False
    output_periods = list()

    # Parse periods by tags
    isFound = False
    prev_rel = None
    for release in reversed(list(repo.get_releases())):
        if isFound is True:
            output_periods.append({'begin': prev_rel.created_at.date(),
                                   'end': release.created_at.date(),
                                   'tag': prev_rel.tag_name})
            prev_rel = None
            isFound = False

        for per in periods:
            if release.tag_name == per:
                isFound = True
                prev_rel = release

    # If there was a last release, then the end date will be today
    if isFound is True:
        output_periods.append({'begin': prev_rel.created_at.date(),
                               'end': datetime.today().date(),
                               'tag': prev_rel.tag_name})

    if output_periods:
        isTags = True

    # Parse periods by dates
    if not output_periods:
        try:
            begin = datetime.strptime(periods[0], '%Y.%m.%d').date()
            end = datetime.strptime(periods[1], '%Y.%m.%d').date()

            while begin < end:
                days = calendar.monthrange(begin.year, begin.month)[1]
                end_tmp = begin + timedelta(days=days)

                output_periods.append({'begin': begin, 'end': end_tmp, 'tag': ''})
                begin = end_tmp

        except Exception as exc:
            sys.exit(exc)

    return isTags, output_periods


# Compare stats by tags (delta)
def compare_releases(stats_array):
    cmp_stats = list()

    iter1, iter2 = tee(stats_array, 2)
    it2 = next(iter2)

    while it2 is not stats_array[-1]:
        it1 = next(iter1)
        it2 = next(iter2)

        stat_tmp = it2 - it1

        stat_tmp.tag = it1.tag + '_' + it2.tag
        stat_tmp.begin = it1.begin
        stat_tmp.end = it2.end

        cmp_stats.append(stat_tmp.copy())

    return cmp_stats


def collect_metric(login_or_token, repo_name, periods, password=None):
    if len(periods) < 2:
        sys.exit('Periods: input 2 dates or 2 or many tags')

    # Connect to github API
    g = github.Github(login_or_token=login_or_token, password=password)
    try:
        g.get_repo(repo_name)
    except Exception as exc:
        sys.exit(exc)

    # Get repository
    repo = g.get_repo(repo_name)

    # Parse period
    isTags, out_periods = parsing_period(repo, periods)
    if not out_periods:
        sys.exit('Periods parse error')

    print('Parsed dates:')
    for per in out_periods:
        print('\t', per['begin'], ' - ', per['end'], per['tag'])

    # Get stats by periods
    stats_array = []
    for per in out_periods:
        print('>> get metric:', per['begin'], ' - ', per['end'])

        stats = GithubStats()
        stats.get_stat(repo, per['begin'], per['end'])
        stats.tag = per['tag']

        stats_array.append(stats.copy())

    # If tags are defined, releases are compare.
    if isTags is True and len(stats_array) != 1:
        return compare_releases(stats_array)

    return stats_array


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--github_username', help='login or token', required=True)
    parser.add_argument('-pw', '--github_password')
    parser.add_argument('-r', '--github_repo', required=True)
    parser.add_argument('-p', '--period', help='release tags or dates(format: year.month.day)', nargs='+',
                        required=True)
    parser.add_argument('-ocv', '--export_opencv', help='save contents in OpenCV format', action='store_true')
    parser.add_argument('-csv', '--export_csv', help='export content to CSV file', action='store_true')
    parser.add_argument('-gdoc', '--export_gdoc', help='export content to Google Drive', action='store_true')

    args = parser.parse_args()

    # Get metric
    stats_array = collect_metric(login_or_token=args.github_username, password=args.github_password,
                                 repo_name=args.github_repo, periods=args.period)

    # Create name output file
    output_name = 'stat'
    for per in args.period:
        output_name += '_' + per

    # Show stats
    for stats in stats_array:
        stats.show()

    print('\n')

    # Save to OpenCV format
    if args.export_opencv is True:
        write_opencv(output_name + '.yml', stats_array)

    # Save to csv format
    if args.export_csv is True or \
            args.export_gdoc is True:
        write_csv(output_name + '.csv', stats_array)

    # Save to Google Drive
    if args.export_gdoc is True:
        write_gdocs(output_name + '.csv', stats_array)


if __name__ == "__main__":
    main()
