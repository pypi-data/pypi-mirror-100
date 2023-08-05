from distutils.core import setup

setup(
    name = 'pyFlarum',
    packages = ['pyflarum'],
    version = 'v0.1-alpha',
    license='GPLv3',
    description = "An unofficial Python package for manipulating with Flarum's API",
    keywords = ['Flarum', 'forum software', 'api', "Flarum api", "bot", "userbot"],

    author = 'Kevo',
    author_email = 'me@kevo.link',

    url = 'https://github.com/CWKevo/pyflarum',
    download_url = 'https://codeload.github.com/CWKevo/pyflarum/zip/v0.1-alpha',

    install_requires=[
        'requests',
        'requests_cache',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
