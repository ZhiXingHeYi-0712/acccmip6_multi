"""A setuptools based setup module for acccmip6"""
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'pandas',
    'requests',
    'setuptools',
    'xlrd',
]

test_requirements = [
    'pytest',
    'requests',
]

setup(
    name='acccmip6_multi',
    version='1.0.0',
    description="Package for accessing CMIP6 database in real-time, download in multi-thread way",
    long_description=readme,
    author="ZhiXingHeYi-0712",
    author_email='Lihao.0712@outlook.com',
    url='https://github.com/ZhiXingHeYi-0712/acccmip6_multi',
    packages=find_packages(exclude=['docs', 'tests']),
    package_data = {
            'utilities':['data/*.xlsx'],
            },
    entry_points={
        'console_scripts':[
            'acccmip6=acccmip6.cli:main',
            ],
        },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
