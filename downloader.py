import re
import argparse

import requests
from bs4 import BeautifulSoup

from leagues import URLS as LEAGUES_URLS

BASE_URL = 'http://www.sportslogos.net/'


class DownloadError(Exception):
    pass


class HtmlParserError(Exception):
    pass


class Downloader(object):

    def __init__(self, sport, league, team_name):
        for arg in [sport, league, team_name]:
            if not isinstance(arg, str):
                raise TypeError('{} must be str, e.g. \'baseball\''.format(
                    arg))

        if sport.lower() not in [s.lower() for s in LEAGUES_URLS.keys()]:
            raise ValueError(
                'sport must be one from "{}"'.format(
                    ', '.join(LEAGUES_URLS.keys())))
        self.sport = sport.lower()

        if league.lower() not in [
                l.lower() for l in LEAGUES_URLS.get(self.sport).keys()]:
            raise ValueError('league must be one from "{}"'.format(
                ', '.join(LEAGUES_URLS.get(self.sport).keys())))
        self.league = league
        self.team_name = team_name
        self.url = '{}{}'.format(
            BASE_URL,
            LEAGUES_URLS.get(self.sport).get(self.league).get('url'))
        self.league_teams = None

    def _get_page(self, url):
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise DownloadError('Filed to download "{}": "{}"'.format(
                url, r.status_code))
        return r.content

    def _get_logo_groups(self, url=None):
        if url is None:
            url = self.url
        page = self._get_page(url)
        parser = BeautifulSoup(page, 'html.parser')
        logos_groups = parser.findAll('ul', {'class': 'logoWall'})
        if len(logos_groups) == 0:
            raise HtmlParserError(
                'Can not find logos list with "logoWall" class')
        return logos_groups

    def _parse_logos_wrapper(self, group):
        logos = group.findAll('li')
        names = {}
        for l in logos:
            link = l.find('a')
            if not link:
                raise HtmlParserError(
                    'Can not find logo link')
            name = link.text
            if not name:
                raise HtmlParserError(
                    'Can not find team name in the logo link')
            name = name.strip().lower()
            name = re.sub(' +', ' ', name)
            url = link.attrs.get('href')
            if not url.startswith(BASE_URL):
                if url.startswith('/'):
                    url = url[1:]
                url = '{}{}'.format(BASE_URL, url)
            names[name] = url
        return names

    def _get_league_teams(self):
        logos = self._get_logo_groups()
        self.league_teams = self._parse_logos_wrapper(logos[0])

    def find_team(self, team_name=None):
        if team_name:
            if not isinstance(team_name, str):
                raise TypeError(
                    '{} must be str, e.g. \'Boston Celtics\''.format(
                        team_name))
        else:
            team_name = self.team_name

        if self.league_teams is None:
            self._get_league_teams()
        teams = self.league_teams
        if team_name.lower() not in teams.keys():
            raise HtmlParserError(
                'Can not find team "{}" at the "{}" league'.format(
                    team_name, self.league))
        team = teams.get(team_name.lower())
        return team

    def get_team_logos(self, team_url):
        logos_groups = self._get_logo_groups(team_url)
        prim_logos = self._parse_logos_wrapper(logos_groups[0])
        try:
            alt_logos = self._parse_logos_wrapper(logos_groups[1])
        except IndexError:
            alt_logos = None
        return {'primary_logos': prim_logos, 'alternate_logos': alt_logos}

    def get_full_size_logo(self, url):
        page = self._get_page(url)
        parser = BeautifulSoup(page, 'html.parser')
        logo_wrapper = parser.find(id='mainLogo')
        if not logo_wrapper:
            raise HtmlParserError(
                'Can not find logo link')
        img = logo_wrapper.find('img')
        if not img:
            raise HtmlParserError(
                'Can not find logo link')
        return img.attrs.get('src')


def main():
    d = Downloader('hockey', 'KHL', 'Ak Bars Kazan')
    team_link = d.find_team()
    print d.get_team_logos(team_link)
    # d._get_league_teams()
    # print d.league_teams.keys()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('sport', help='sport type, e.g. "baseball"')
    parser.add_argument('league', help='abbr of sport league')
    parser.add_argument('team', help='sport team name', type=str, nargs=1)
    parser.add_argument('-s', '--search', help='search team in league',
                        action='store_true')
    parser.add_argument('-p', '--path', help='save logo to a custom path',
                        action='store', type=str, nargs=1)
    args = parser.parse_args()
    # main()
