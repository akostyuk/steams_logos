steams_logos
============
[![Build Status](https://travis-ci.org/akostyuk/steams_logos.svg?branch=master)](https://travis-ci.org/akostyuk/steams_logos)

This is simple sport teams logo extraction tool from http://www.sportslogos.net/

Requirements
------------
* requests
* beautifulsoup4

Installation
------------
This is just a "POC" project and I don't planning to add it to the PyPI.
You can always install the latest master branch directly from gihub using pip:

```zsh
pip install https://github.com/akostyuk/steams_logos/archive/master.zip
```

Usage
-----
After installation you can use the **Downloader** class or **slogos** command-line tool.

### command-line tools
This command will download the primary image for the San Antonio Spurs:
```zsh
slogos basketball NBA 'San Antonio Spurs'
```

You can use **slogos-helper** command line tools to list all available leagues for specific sport type:
```zsh
slogos-helper --readable basketball
```

### directly from your code
```python
from steams_logos import Downloader


d = Downloader('basketball', 'NBA', 'San Antonio Spurs')
team_link = d.find_team()
logos = d.get_team_logos(team_link)
primary_logo = None
for n, url in logos.get('primary_logos').items():
    if n.endswith('pres'):
        primary_logo = url
        break
full_size_logo = d.get_full_size_logo(primary_logo)
d.download(full_size_logo)
```

Tests
-----
```zsh
python setup.py test
```

License
-------
MIT
