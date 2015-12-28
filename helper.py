# This is helper module with usefull functions
#
# - get_ligues() returns a disctionary with all available ligues for specific
#   sport type
#

import re
import pprint
import argparse

from downloader import Downloader, BASE_URL, HtmlParserError
from meta import REPLACES, EXCLUDES

SPORTS_URLS = {
    'baseball': 'leagues/list_by_sport/2/Baseball/logos',
    'basketball': 'leagues/list_by_sport/3/Basketball/logos',
    'hockey': 'leagues/list_by_sport/1/Hockey/logos',
    'football': 'leagues/list_by_sport/4/Football/logos',
    'soccer': 'leagues/list_by_sport/5/Soccer/logos'
}


class ExtendedDownloader(Downloader):

    def __init__(self, sport):
        self.sport = sport.lower()
        self.league_teams = None

    def _extract_abbr(self, url):
        names = url.split('/')
        names = [x for x in names if x]
        abbr = names[-2]
        replaces = REPLACES.get(self.sport)
        if abbr in replaces.keys():
            abbr = replaces[abbr]
        return abbr.upper()

    def _parse_logos_wrapper(self, group):
        logos = group.findAll('li')
        names = {}
        for l in logos:
            t = l.get_text()
            if not t.strip().endswith('Pres'):
                continue
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


def get_ligues(sport):
    summary = {}
    d = ExtendedDownloader(sport)
    groups = d._get_logo_groups(
        '{}{}'.format(BASE_URL, SPORTS_URLS.get(sport)))
    excludes = EXCLUDES.get(d.sport)
    for g in groups:
        leagues = d._parse_logos_wrapper(g)
        for name, url in leagues.iteritems():
            if excludes and name in excludes:
                continue
            abbr = d._extract_abbr(url)
            summary[abbr] = {
                'description': name.title(),
                'url': url.replace(BASE_URL, '')
            }
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Display dictionary of leagues for a sport type')
    parser.add_argument('sport', help='sport type, e.g. "baseball"')
    parser.add_argument('--readable', help='display sport leagues pairs'
                        ' (abbr - description) in readable format',
                        action='store_true')
    args = parser.parse_args()
    sports = SPORTS_URLS.keys()
    if args.sport not in sports:
        print ('"{}" is a wrong sport type. Sport type should be one'
               ' of the following: "{}"'.format(args.sport, ', '.join(sports)))
    else:
        ligues = get_ligues(args.sport.lower())
        if args.readable:
            for a, data in ligues.iteritems():
                print u'{} - {}'.format(a, data.get('description'))
        else:
            pprint.pprint(ligues, width=70)
