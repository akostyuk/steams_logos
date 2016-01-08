import os
from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_reqs = parse_requirements('requirements.txt', session=PipSession)
reqs = [str(ir.req) for ir in install_reqs]


setup(
    name='steams_logos',
    version='0.0.1',
    author='Alexey Kostyuk',
    author_email='unitoff+steamslogos@gmail.com',
    description=('Simple package that allows to extract sport teams logos '
                 'from www.sportslogos.net'),
    license='MIT',
    keywords='sportslogos.net sport teams logos',
    url='https://github.com/akostyuk/steams_logos',
    packages=['steams_logos'],
    long_description=read('README.md'),
    install_requires=reqs,
    scripts=['bin/slogos', 'bin/slogos-helper'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
