#!/usr/bin/env python3

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


setup(
    name='pymata4',
    packages=['pymata4'],
    install_requires=['pyserial'],

    version='1.8',
    description="A Python Protocol Abstraction Library For Arduino Firmata",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    url='https://github.com/MrYsLab/pymata4',
    download_url='https://github.com/MrYsLab/pymata4',
    keywords=['Firmata', 'Arduino', 'Protocol', 'Python'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

