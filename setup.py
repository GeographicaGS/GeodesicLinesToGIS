# -*- coding: utf-8 -*-

# This file is part of GeodesicLinesToGIS.
# https://github.com/GeographicaGS/GeodesicLinesToGIS

# Licensed under the GPLv2 license:
# https://www.gnu.org/licenses/gpl-2.0.txt
# Copyright (c) 2015-2017, Cayetano Benavent <cayetanobv@gmail.com>

from setuptools import setup, find_packages


# Get the long description from README file.
# Before upload a new version run rstgenerator.sh
# to update Readme reStructuredText file from
# original Readme markdown file.
with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='GeodesicLinesToGIS',
    version='0.4.3',

    description='Computes geodesic lines from start point to end point and stores them in a GIS file (Shapefile and GeoJSON). The problem of geodesic lines crossing antimeridian is solved.',
    long_description=long_description,

    author='Cayetano Benavent',
    author_email='cayetano.benavent@geographica.gs',

    # The project's main homepage.
    url='http://github.com/GeographicaGS/GeodesicLinesToGIS',

    # Licensed under the GPLv2 license:
    # https://www.gnu.org/licenses/gpl-2.0.txt
    license='GPLv2',

    # According to: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS'
    ],

    keywords='geodesic GIS antimeridian',

    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'pyproj>=1.9.3,<1.10',
        'fiona>=1.5.0,<2.0',
        'shapely>=1.5.0,<2.0'
    ]

)
