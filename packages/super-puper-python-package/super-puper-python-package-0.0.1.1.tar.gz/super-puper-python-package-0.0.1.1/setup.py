#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: DanilaCharushin
:license: MIT License
:copyright: (c) 2021 DanilaCharushin
"""

version = '0.0.1.1'

description = """
So, I hope you leave this repo, it's for test.
"""


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='super-puper-python-package',
    version=version,
    author='DanilaCharushin',
    author_email='charushin2000@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DanilaCharushin/super-puper-python-package',
    download_url='https://github.com/DanilaCharushin/super-puper-python-package/archive/master.zip',
    license='MIT License',
    packages=['super_puper_python_package'],
    install_requires=['loguru'],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)