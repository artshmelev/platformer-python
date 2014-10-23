# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

setup(
    name='Platformer',
    version='1.0',
    packages=find_packages(),
    description='Platformer like Mario on Python',
    author='Artem Shmelev, Sergey Omelchenko',
    author_email='artem.shmelev@gmail.com',
    url='https://github.com/artshmelev/platformer-python',
    license='MIT',
    entry_points = {
        'console_scripts': [
            'platformer-python = platformer_python.client:main',
            'platformer-python-server = platformer_python.server:main',
        ],
    },
    package_data = {
        '': [
            'graphics/*',
            'sounds/*',
        ],
    },
    include_package_data=True,
    install_requires=['pygame'],
)
