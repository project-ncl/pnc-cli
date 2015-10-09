from setuptools import setup
from setuptools import find_packages
import os
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
setup(
    name='pnc-cli',
    packages=find_packages(exclude=['test*']),
    version='0.0.2',
    description='CLI wrapper for PNC REST calls',
    author = 'Tom Hauser',
    author_email = 'thauser@redhat.com',
    url = 'https://github.com/thauser/pnc_cli',
    download_url='https://github.com/thauser/pnc_cli/tarball/pypi-0.0.2',
    keywords = ['PNC','REST'],
    long_description=README,
    install_requires=[
	    "argh >= 0.26.1",
        "requests >= 2.4.3",
        "certifi >= 2015.04.28",
        'mock'
    ],
    classifiers=[
	'Development Status :: 3 - Alpha',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3'
    ],
    entry_points={'console_scripts': ['pnc = pnc_cli.pnc:main']}
)
