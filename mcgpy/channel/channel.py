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

'''channel : a utility to read the sensor information from a configuration file or a raw file.
'''

import sys
import os
import configparser
import h5py
from astropy.table import QTable

__author__ = 'Phil Jung <pjjung@amcg.kr>'
__all__ = ['ChannelConfig', 'ChannelActive']

#---- class of reading fundamental channel information from configuration file --------------------------------
class ChannelConfig:
  def __init__(self, path):
    '''Read the information of sensor posirion, direction, number and label from a channel configuration file.
    
    Parameters
    ----------
    path : "string"
        input path must be .ini format and include sensor information of MCG system
        
    Raises
    ------
    IOError
        if a "str" input is not a configuration file path
        
    TypeError
        if a configuration file did not match a specific format
    '''
    
    self.path = path
    self._io_checker(self.path)
    self._section_checker(self.path)
  
  ##---- Moethods -------------------------------- 
  def get(self, key):
    '''Provide the information by the given key.
    
    Parameters
    ----------
    key : "string"
        the key takes "Label", "Position", or "Positions"
        
    Return
    ------
    table : "astropy.table.QTable"
        the sensor information as astropy QTable
    
    Examples
    --------
    >>> from mcgpy.channel import ChannelConfig
    >>> config = ChanngelConfig('~/test/file/path.ini')
    >>> config.get("label")
    number	label
    int64	str3
    1	    label_1
    2	    label_2
    3	    label_3
    .
    .
    .
    
    >>> config.get("positions")
    number	positions
    int64	float64
    1	    (x1, y1, z1)
    2	    (x2, y2, z2)
    3	    (x3, y3, z3)
    .
    .
    .
    '''
    
    return self._make_table(key)

  ##---- Inherent properties -------------------------------- 
  def _io_checker(self, path):
    if os.path.isfile(path) != True and path.split('.')[-1] != 'ini':
      raise IOError('illegal file format was inserted')
      
  def _section_checker(self, path):
    _fundamental_keys = ['Label', 'Positions', 'Directions']
    config = configparser.RawConfigParser()
    config.read(path)
    for key in config.__dict__['_sections']:
      if not key.capitalize() in _fundamental_keys:
        raise TypeError('sections in the configuration file must be consisted of "Label", "Positions", and "Directions".')
    
  def _get_items(self, key):
    config = configparser.RawConfigParser()
    config.read(self.path)
    try:
      return config.items(key)
    except:
      return config.items(key.capitalize())
    else:
      raise KeyError(key)

  def _make_table(self, key):
    items = self._get_items(key)
    
    if key.capitalize() == 'Label':
      _keys, _values = list(), list()
      for _key, _value in items:
        _keys.append(int(_key))
        _values.append(_value)
      
    elif key.capitalize() == 'Positions' or key.capitalize() == 'Directions':
      _keys, _values = list(), list()
      for _key, _value in items:
        _keys.append(int(_key))
        _values.append([float(number) for number in _value.split(',')])
        
    return QTable([_keys, _values], names=('number', key))
      
    
#---- class of reading activated channel list from frame file --------------------------------
class ChannelActive:
  def __init__(self, path):
    '''Read the information of active sensor number and label from raw files,
       for raw files contained active channel data only, 
       
    Parameters
    ----------
    path : "string"
        input path must be .kdf or .hdf5 format
    
    Raises
    ------
    IOError
        if a "str" input is not a raw file path: .kdf or .hdf5
    '''
    
    self.path = path
    self.extension = self._io_checker(self.path)
  
  ##---- Moethods -------------------------------- 
  def get_table(self):
    '''Provide activie channel's number and label as "astropy.tabel.QTable"
    
    Return
    ------
    table : "astropy.table.QTable"
        the active sensor information as astropy QTable 
    
    Examples
    --------
    >>> from mcgpy.channel import ChannelActive
    >>> activated = ChannelActive("~/test/raw/file/path.hdf5")
    >>> activated.get_table()
    number	label
    int64	str3
    1	    label_1
    2	    label_2
    4	    label_4
    10	    label_10
    11	    label_11
    .
    .  
    '''
    
    if self.extension == 'kdf':
      return self._kdf()
    
    elif self.extension == 'hdf5':
      return self._hdf()
    
  def get_number(self):
    '''Provide active channel's number as "list"
    
    Return
    ------
    list : "list"
        the active sensor's number as list 
    
    Example
    -------
    >>> from mcgpy.channel import ChannelActive
    >>> activated = ChannelActive("~/test/raw/file/path.hdf5")
    >>> activated.get_number()
    [1,2,4,10,11,...]
    '''
    
    if self.extension == 'kdf':
      return list(self._kdf()['number'])
    
    elif self.extension == 'hdf5':
      return list(self._hdf()['number']) 
    
  def get_label(self):
    '''Provide active channel's label as "list"
    
    Return
    ------
    list : "list"
        the active sensor's label as list 
    
    Example
    -------
    >>> from mcgpy.channel import ChannelActive
    >>> activated = ChannelActive("~/test/raw/file/path.hdf5")
    >>> activated.get_label()
    [label_1,label_2,label_4,label_10,label_11,...]
    '''
    
    if self.extension == 'kdf':
      return list(self._kdf()['label'])
    
    elif self.extension == 'hdf5':
      return list(self._hdf()['label']) 
    
  ##---- Inherent properties -------------------------------- 
  def _io_checker(self, path):
    extension = path.split('.')[-1]
    if extension == 'kdf':
      return extension
    elif extension == 'hdf5':
      return extension
    else:
      raise IOError('illegal file format was inserted')
    
  def _make_table(self, items):
    keys, values = list(), list()
    for item in items:
      try:
        Xaxis_label = item.split('X')
        keys.append(int(Xaxis_label[0])+1)
        values.append('X{}'.format(Xaxis_label[1]))

      except ValueError:
        Yaxis_label = item.split('Y')
        keys.append(int(Yaxis_label[0])+1)
        values.append('Y{}'.format(Yaxis_label[1]))
        
    return QTable([keys, values], names=('number', 'label'))
    
  def _kdf(self):
    data_size = os.path.getsize(self.path)
    with open(self.path, 'br') as f:
      number = int(f.read(256)[-4:].decode('ascii'))
      labels_ = f.read(16*number).decode('ascii')
      labels = [labels_[i*16:(i+1)*16].strip() for i in range(number-1)]
    
    return self._make_table(labels)
      
  def _hdf(self):
    with h5py.File(self.path, 'r') as f:
      keys, values = list(), list()
      for groupname in f.keys():
        group = f.get(groupname)
        metadata = group.get('timeseries').attrs

        keys.append(int(groupname.split('_')[0]))
        values.append(groupname.split('_')[1])
        
    return QTable([keys, values], names=('number', 'label'))