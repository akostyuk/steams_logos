import re

import requests
from bs4 import BeautifulSoup

from .leagues import URLS as LEAGUES_URLS

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

    def download(self, url, path=None, name=None):
        ext = url.split('.')[-1]
        if len(ext) > 4:
            ext = 'jpg'
        r = requests.get(url, stream=True)
        if not r.status_code == 200:
            raise DownloadError('Filed to download image "{}": "{}"'.format(
                url, r.status_code))

        if path:
            save_to = path
            if not save_to.endswith('/'):
                save_to = '{}/'.format(save_to)
        else:
            save_to = './'

        if name is None:
            name = '{}-{}-{}'.format(
                self.sport,
                self.league.lower(),
                self.team_name.lower().replace(' ', '-'))

        file_to_save = '{}{}.{}'.format(save_to, name, ext)

        # save logo
        with open(file_to_save, 'w') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return file_to_save


def find_team(sport, league, team_name):
    d = Downloader(sport, league, team_name)
    try:
        team = d.find_team()
        league_name = LEAGUES_URLS.get(sport).get(league).get('description')
        print('Found: {}'.format(team_name))
        print('league: {} ({})'.format(league_name, league))
        print('team link: {}'.format(team))
    except HtmlParserError:
        print('Can not find {} team "{}" in the "{}" league'.format(
              sport, team_name, league))


def download(sport, league, team_name, path=None):
    d = Downloader(sport, league, team_name)
    team_link = d.find_team()
    logos = d.get_team_logos(team_link)
    primary_logo = None
    for n, url in logos.get('primary_logos').items():
        if n.endswith('pres'):
            primary_logo = url
            break
    if primary_logo is None:
        print('Can not find main logo for "{}" team'.format(team_name))
    else:
        full_size_logo = d.get_full_size_logo(primary_logo)
        print('Main logo url: {}'.format(full_size_logo))
        saved = d.download(full_size_logo, path)
        print('Logo has been successfully saved to the file: {}'.format(saved))
