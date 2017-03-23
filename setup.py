#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

EXTRA_REQUIREMENTS = ['python-dateutil', 'simplejson']

def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("thresher/__init__.py")


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='thresher',
    version=__version__,
    description=('A utility to harvest file content from SHARE.'),
    #long_description=read('README.rst'),
    author='Rick Johnson',
    author_email='richardpatrickjohnson@gmail.com',
    url='https://github.com/share-research/thresher',
    packages=find_packages(exclude=('test*', 'examples')),
    package_dir={'thresher': 'thresher'},
    include_package_data=True,
    extras_require={'reco': EXTRA_REQUIREMENTS},
    license='Apache-2.0',
    zip_safe=False,
    keywords=('share', 'rest', 'json', 'api', 'linked data', 'harvest', 'schema'),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education'
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
    #test_suite='tests'
)
