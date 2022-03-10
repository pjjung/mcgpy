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

setup(
      name='MCGpy',
      version='0.1',
      author='Phil Jung',
      author_email='pjjung@amcg.kr',
      description='The MCGpy is the package for studying adta for magnetocardiography, for instrumetnal or medical purpose.',
      packages=find_packages(exclude=['test', 'examples']),
      install_requires=['setuptools', 'numpy', 'scipy', 'astropy', 'h5py', 'matplotlib'],
      python_requires='>=3.7',
      classifiers=['Programing Language :: Python :: 3.9',
                  'License :: OSI Approved :: MIT License',
                  'Operating System :: OS Independent']
      )