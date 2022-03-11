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

'''_array : the core class for wrapping the multi-channel dataset with metadata
'''

import numpy as np

__author__ = 'Phil Jung <pjjung@amcg.kr>'

class Array(np.ndarray):
  def __new__(cls, source, metadata=None):
    '''Convert multi-channel dataset to "np.ndarray" with metadata
    
    Parameters
    ----------
    source : "list" or "np.ndarray"
        Multi-channel time-series dataset.
        If "list" type source is given, it will be converted to "np.ndarray" type,
    
    medadata : "dict", optional
        dictionary consisted of data information recored in the header line of KDF file or matadata of HDF file
        
    Return
    ------
    new : "np.ndarray"
        rows are a channel time-series, and columns are data points
    
    '''
    if isinstance(source, list):
      new = np.asarray(source).view(cls)
    else:
      new = source.view(cls)
    
    if isinstance(metadata, dict):  
      try:
        for key, value in metadata.items():
          cls._set_attribute(key, value)
      except (NameError, TypeError):
        pass
      
    return new
  
  ##---- Properties -------------------------------- 
  # BIOSEMI
  @property
  def biosemi(self):
    try:
      return self._biosemi
    except AttributeError:
      self._biosemi = None
      return self._biosemi
  
  # info
  @property
  def info(self):
    try:
      return self._info
    except AttributeError:
      self._info = None
      return self._info
  
  # sample rate
  @property
  def sample_rate(self):
    try:
      return self._sample_rate
    except AttributeError:
      self._sample_rate = None
      return self._sample_rate
    
  # number
  @property
  def number(self):
    try:
      return self._number
    except AttributeError:
      self._number = None
      return self._number
  
  # label
  @property
  def label(self):
    try:
      return self._label
    except AttributeError:
      self._label = None
      return self._label
  
  # t0
  @property
  def t0(self):
    try:
      return self._t0
    except AttributeError:
      self._t0 = None
      return self._t0
  
  # duration
  @property
  def duration(self):
    try:
      return self._duration
    except AttributeError:
      self._duration = None
      return self._duration
  
  # datetime
  @property
  def datetime(self):
    try:
      return self._datetime
    except AttributeError:
      self._datetime = None
      return self._datetime
  
  # position
  @property
  def position(self):
    try:
      return self._position
    except AttributeError:
      self._position = None
      return self._position
  
  @position.setter
  def position(self, value):
    self._set_attribute('position', value)
    
  @position.deleter
  def position(self):
    try:
      del self._position
    except AttributeError:
      pass
    
  # direction
  @property
  def direction(self):
    try:
      return self._direction
    except AttributeError:
      self._direction = None
      return self._direction
  
  @direction.setter
  def direction(self, value):
    self._set_attribute('direction', value)
    
  @direction.deleter
  def direction(self):
    try:
      del self._direction
    except AttributeError:
      pass
  
  ##---- Inherent properties -------------------------------- 
  @classmethod
  def _set_attribute(cls, key, value):
    _key = '_{}'.format(key)
    try:
      current_attribute = getattr(cls, _key)
      if (value is None 
          or value != current_attribute
          or getattr(cls, key) is None):
        delattr(cls, _key)
        setattr(cls, _key, value)
    except AttributeError:
      setattr(cls, _key, value)