import pytest
from steams_logos import Downloader
from steams_logos.downloader import (
    DownloadError, HtmlParserError, BASE_URL, find_team)


class FakeResponse(object):
    def __init__(self, status_code=200, content=''):
        self.status_code = status_code
        self.content = content


def test_downloader_init_wrong_args_type():
    with pytest.raises(TypeError):
        Downloader(0, 'string', {})


def test_downloader_init_wrong_sport():
    with pytest.raises(ValueError):
        Downloader('fake', 'NBA', 'fake')


def test_downloader_init_wrong_league():
    with pytest.raises(ValueError):
        Downloader('basketball', 'fake', 'fake')


def test_download_error(monkeypatch):
    monkeypatch.setattr(
        'requests.get', lambda x, stream: FakeResponse(status_code=404))
    d = Downloader('basketball', 'NBA', 'Fake Team')
    with pytest.raises(DownloadError):
        d.find_team()


def test_html_parser_error(monkeypatch):
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse())
    d = Downloader('basketball', 'NBA', 'Fake Team')
    with pytest.raises(HtmlParserError):
        d.find_team()


def test_parse_logos_wrapper_wrong_link(monkeypatch):
    d = Downloader('basketball', 'NBA', 'Fake Team')
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<ul class="logoWall">'
        '<li>no link</li></ul>'))
    logos = d._get_logo_groups()
    with pytest.raises(HtmlParserError):
        d._parse_logos_wrapper(logos[0])


def test_parse_logos_wrapper_wrong_name(monkeypatch):
    d = Downloader('basketball', 'NBA', 'Fake Team')
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<ul class="logoWall">'
        '<li><a href="#"></a></li></ul>'))
    logos = d._get_logo_groups()
    with pytest.raises(HtmlParserError):
        d._parse_logos_wrapper(logos[0])


def test_parse_logos_wrapper_link(monkeypatch):
    d = Downloader('basketball', 'NBA', 'Fake Team')
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<ul class="logoWall">'
        '<li><a href="/test">Fake Team</a></li></ul>'))
    logos = d._get_logo_groups()
    n = d._parse_logos_wrapper(logos[0])
    assert n['fake team'].endswith('/test')


def test_find_team_wrong_type():
    d = Downloader('basketball', 'NBA', 'test')
    with pytest.raises(TypeError):
        d.find_team(team_name=int('10'))


def test_find_team_not_exist():
    d = Downloader('basketball', 'NBA', 'test')
    with pytest.raises(HtmlParserError):
        d.find_team()


def test_find_team(monkeypatch):
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<ul class="logoWall">'
        '<li><a href="#">Fake Team</a></li></ul>'))
    d = Downloader('basketball', 'NBA', 'Fake Team')
    url = d.find_team()
    assert url == '{}#'.format(BASE_URL)


def test_get_team_logos_alt_logos_none(monkeypatch):
    d = Downloader('basketball', 'NBA', 'Fake Team')
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<ul class="logoWall">'
        '<li><a href="#2002-2003">2002/03 - 2003/03</a></li>'
        '<li><a href="#2003-pres">2003/03 - Pres</a></li>'
        '</ul>'))
    logos = d.get_team_logos('#')
    assert logos['alternate_logos'] is None


def test_get_team_logos(monkeypatch):
    d = Downloader('basketball', 'NBA', 'Fake Team')
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<ul class="logoWall">'
        '<li><a href="#2002-2003">2002/03 - 2003/03</a></li>'
        '<li><a href="#2003-pres">2003/03 - Pres</a></li>'
        '</ul><ul class="logoWall">'
        '<li><a href="#2002-2003">2002/03 - 2003/03</a></li>'
        '<li><a href="#2003-pres">2003/03 - Pres</a></li>'
        '</ul>'))
    logos = d.get_team_logos('#')
    for i in ('alternate_logos', 'primary_logos'):
        assert i in logos.keys()
    assert 2 == len(logos['primary_logos'])
    assert 2 == len(logos['alternate_logos'])


def test_get_full_size_logo_id_not_exist(monkeypatch):
    d = Downloader('basketball', 'NBA', 'Fake Team')
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<div><img src="fake_team_url"></div>'))
    with pytest.raises(HtmlParserError):
        d.get_full_size_logo('#')


def test_get_full_size_logo_img_not_exist(monkeypatch):
    d = Downloader('basketball', 'NBA', 'Fake Team')
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<div id="mainLogo"></div>'))
    with pytest.raises(HtmlParserError):
        d.get_full_size_logo('#')


def test_get_full_size_logo(monkeypatch):
    d = Downloader('basketball', 'NBA', 'Fake Team')
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<div id="mainLogo"><img src="fake_team_url"></div>'))
    l = d.get_full_size_logo('#')
    assert l == 'fake_team_url'


def test_find_team_not_exist_func(monkeypatch, capsys):
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<ul class="logoWall">'
        '<li><a href="#"></a></li></ul>'))
    find_team('basketball', 'NBA', 'Fake Team')
    out, err = capsys.readouterr()
    assert out.startswith('Can not find basketball team')


def test_find_team_func(monkeypatch, capsys):
    monkeypatch.setattr('requests.get', lambda x, stream: FakeResponse(
        content='<ul class="logoWall">'
        '<li><a href="#">Fake Team</a></li></ul>'))
    find_team('basketball', 'NBA', 'Fake Team')
    out, err = capsys.readouterr()
    assert out.startswith('Found:')

# def test_find_team_not_exist_func():
#     pass
