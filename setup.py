from distutils.core import setup
setup(
    name='pnc-cli',
    packages=['pnc-cli'],
    version='0.1',
    description='CLI wrapper for PNC REST calls',
    author = 'Tom Hauser',
    author_email = 'thauser@redhat.com',
    url = 'https://github.com/thauser/pnc-cli',
    download_url='',
    keywords = ['PNC','REST'],
    long_description=open('README.md').read(),
    install_requires=[
	"argh >= 0.26.1",
        "requests >= 2.4.3"
    ]
)
