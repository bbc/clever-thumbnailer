# Copyright (C) 2015 British Broadcasting Corporation
#
# Cleverthumbnailer is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# Cleverthumbnailer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cleverthumbnailer; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from setuptools import setup

setup(
    name='cleverthumbnailer',
    version='0.1.0',
    description='Selects interesting and relevant short thumbnails for '
                'longer audio tracks',
    author='Jon Tutcher',
    author_email='jon.tutcher@bbc.co.uk',
    packages=['cleverthumbnailer', 'cleverthumbnailer.featureextractor'],
    entry_points={
        'console_scripts': [
            'cleverthumbnailer = cleverthumbnailer.__main__:main'
        ]
    },
    install_requires=[
        'numpy',
        'qmsegmenter',
        'appdirs',
        'enum',
        'logging',
        'argparse',
        'wave',
        'appdirs',
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 or ' +
        'later (GPLv2+)'
    ]
)
