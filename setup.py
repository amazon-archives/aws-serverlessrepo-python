"""A setuptools based setup module."""

from io import open
from os import path
from setuptools import setup, find_packages

# Required packages for this module to work
REQUIRED = [
    'pyyaml~=5.1',
    'boto3~=1.9, >=1.9.56',
    'six~=1.11'
]

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(path.join(here, 'serverlessrepo', '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    keywords="AWS Serverless Application Repository",
    packages=find_packages(exclude=['tests', 'docs']),
    # Support Python 2.7 and 3.4 or greater
    python_requires=(
        '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'
    ),
    install_requires=REQUIRED,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
    ]
)
