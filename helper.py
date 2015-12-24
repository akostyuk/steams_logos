import re
import pprint
import argparse

from downloader import Downloader, BASE_URL, HtmlParserError
from meta import REPLACES, EXCLUDES

SPORTS_URLS = {
    'baseball': '',
    'basketball': '',
    'hockey': '',
    'football': '',
}


class ExtendedDownloader(Downloader):

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


def main():
    summary = {}
    d = ExtendedDownloader('baseball', 'AL', 'test')
    groups = d._get_logo_groups(
        '{}leagues/list_by_sport/3/Basketball/logos'.format(BASE_URL))
    excludes = EXCLUDES.get(d.sport)
    for g in groups:
        leagues = d._parse_logos_wrapper(g)
        for name, url in leagues.iteritems():
            if name in excludes:
                continue
            abbr = d._extract_abbr(url)
            summary[abbr] = {
                'description': name.title(),
                'url': url.replace(BASE_URL, '')
            }
    pprint.pprint(summary, width=70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Display dictionary of leagues for a sport type')
    parser.add_argument('sport', help='sport type, e.g. "baseball"')
    args = parser.parse_args()
    sports = SPORTS_URLS.keys()
    if args.sport not in sports:
        print ('"{}" is a wrong sport type. Sport type should be one'
               ' of the following: "{}"'.format(args.sport, ', '.join(sports)))
    else:
        # main()
        pass
