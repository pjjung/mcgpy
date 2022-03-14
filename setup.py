# -*- coding: utf-8 -*-
# Copyright (C) Phil Jung (2022)
#
# This file is port of MCGpy.
#
# MCGpy package consists of classes and methods for studying data from magnetocardiography (MCG) 
# and is designed for what users do not care how the code works, but utilize it 
# for instrumental or medical purposes as easy-to-use.
#
# MCGpy is following the GNU General Public License version 3. Under this term, you can redistribute and/or modify it.
# See the GNU free software license for more details.

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
      name='MCGpy',
      version='0.1.1',
      author='Phil Jung',
      author_email='pjjung@amcg.kr',
      description='The MCGpy is the package for studying magnetocardiography data, for instrumetnal or medical purpose.',
      url='https://github.com/pjjung/mcgpy',
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords=['mcgpy','magnetocardiography'],
      packages=find_packages(exclude=['test', 'examples']),
      install_requires=['setuptools', 'numpy', 'scipy', 'astropy', 'h5py', 'matplotlib'],
      python_requires='>=3.6',
      classifiers=['Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
                   'Operating System :: OS Independent']
      )
