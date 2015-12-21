import re

from downloader import Downloader, BASE_URL, HtmlParserError


class ExtendedDownloader(Downloader):

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
    d = ExtendedDownloader('hockey', 'NHL', 'test')
    groups = d._get_logo_groups('http://www.sportslogos.net/leagues/list_by_sport/2/Baseball')
    for g in groups:
        print d._parse_logos_wrapper(g)


if __name__ == "__main__":
    main()
