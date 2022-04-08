# -*- coding: utf-8 -*-
# Copyright (C) Phil Jung (2022)
#
# This file is part of MCGpy.
#
# MCGpy package consists of classes and methods for studying data from magnetocardiography (MCG) 
# and is designed for what users do not care how the code works, but utilize it 
# for instrumental or medical purposes as easy-to-use.
#
# MCGpy is following the GNU General Public License version 3. Under this term, you can redistribute and/or modify it.
# See the GNU free software license for more details.

'''_hdf5 : the class to read an HDF5 file and convert it to "mcgpy.Array" 
'''

import os
import h5py
import numpy as np

from ._array import Array

__author__ = 'Phil Jung <pjjung@amcg.kr>'

#---- main class --------------------------------
class HDF:
  def __init__(self, path, *args ,**kwargs):
    '''initialize arguments and check the reliability
    
    Parameters
    ----------
    path : "str"
        the direction of a HDF5 file
    
    Raises
    ------
    IOError
        if the given file direction did not exist or did not a HDF5 format
    '''
    
    self.path = path
    self._io_checker(self.path)
  
  ##---- Methods -------------------------------- 
  def read(self, number=None, label=None, *args ,**kwargs):
    '''choose time-series data of single-channel by the number or the label
    
    Parameters
    ----------
    number : "int"
        the number of a channel
    
    label :"str"
        the label of a channel
    
    Return
    ------
    Array : "mcgpy.Array"
        a single-channel time-series dataset with meta information
    
    Raises
    ------
    ValueError
        if a wrong number or lavel was given
    
    TypeError
        if both arguments were given, or ware None
    '''

    timeseries, metadata = self._get_data(number, label)
    
    return Array(timeseries, metadata)
  
  ##---- Inherent functions -------------------------------- 
  def _io_checker(self, path):
    extension = path.split('.')[-1]
    if os.path.isfile(path) and extension.lower() != 'hdf5':
      raise IOError('illegal file format was inserted')
      
  def _get_data(self, number=None, label=None):
    groupname = self._parameter_checker(number, label)
    with h5py.File(self.path, 'r') as f:
      group = f.get(groupname)
      timeseries = np.array(group.get('timeseries'))

      metadata = dict(group.get('timeseries').attrs)
      metadata['position'] = tuple(group.get('position'))
      metadata['direction'] = tuple(group.get('direction'))
      
    return timeseries, metadata
      
  def _get_groupnames(self):
    numbers, labels, groupnames = list(), list(), list()
    with h5py.File(self.path, 'r') as f:
      for key in f.keys():
        number, label = int(key.split('_')[0]), key.split('_')[1]
        numbers.append(number)
        labels.append(label)
        groupnames.append(key)
    return numbers, labels, groupnames
  
  def _parameter_checker(self, number, label):
    numbers, labels, groupnames = self._get_groupnames()
    if number is not None and label is None:
      if number in numbers:
        index = numbers.index(number)
        return groupnames[index]
      else:
        raise ValueError('{}-number channel did not exist in given HDF file'.format(number))
      
    elif number is None and label is not None:
      if label in labels:
        index = labels.index(label)
        return groupnames[index]
      else:
        raise ValueError('{} channel did not exist in given HDF file'.format(label))
      
    elif number is not None and label is not None:
      raise TypeError('read method task 1 positional argument but 2 ware given')
      
    else:
      raise TypeError('read method missing 1 required positional argument: "number" or "label"')
