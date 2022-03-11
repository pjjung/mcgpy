# -*- coding: utf-8 -*-
# Copyright (C) Phil Jung (2022)
#
# This file is part of MCGpy.
# The fundamental concept and idea of the 'Series' class are based on the part of GWpy,
# developed by Duncan Macleod <duncan.macleod@ligo.org>.
#
# MCGpy package consists of classes and methods for studying data from magnetocardiography (MCG) 
# and is designed for what users do not care how the code works, but utilize it 
# for instrumental or medical purposes as easy-to-use.
#
# MCGpy is following the GNU General Public License version 3. Under this term, you can redistribute and/or modify it.
# See the GNU free software license for more details.

'''series : a class to build series dataset
'''

import numpy as np
from astropy.units import (second, Quantity, Unit)
from warnings import warn

__author__ = 'Phil Jung <pjjung@amcg.kr>'

class Series(Quantity):
  _default_yunit = Unit('tesla')*10**-15 #femto tesla [fT]
  _default_xunit = second #second [s]
  
  def __new__(cls, value, unit=None, x0=None, dx=None, xindex=None, xunit=None, **kwargs):
    '''build series dataset
    
    Parameters
    ----------
    value : "list", "np.ndarray", "astropy.units.Quantity"
        series dataset
        
    unit : "astropy.units.Quantity", optional
        unit of series,
        if given value is None, it will be set to time-series default unit
    
    x0 : "astropy.units.Quantity", optional
        start point of xidex,
        if given value is None, it will be set to 0
    
    dx : "astropy.units.Quantity", optional
        interval between xindex,
        if given valeu is None, it will be set to 1
        
    xindex : "list", "np.ndarray", "astropy.units.Quantity"
        x-index of seires,
        if given value is None, it will be built based on x0 and dx
        
    xunit : "astropy.units.Quantity", optional
        unit of xindex,
        if given value is None, it will be set to time-series default unit

    Return : "mcgpy.series.Series"
    ------
        series array
    
    Examples
    --------
    >>> from mcgpy.series import Series
    >>> from astropy.units import (Unit, second)
    >>> import numpy as np
    >>> data = np.random.random(100)
    >>> Series(data, unit=1*Unit('volt'), x0=0, dx=1/512, xunit=second)
    [0.8783319, 0.16395352, ..., 0.17695802, 0.46733861] V
    >>> Series(data, unit=1*Unit('volt'), x0=0, dx=1/512, xunit=second).xindex
    [0, 0.001953125, 0.00390625, ..., 0.19140625, 0.19335938] s
    '''
    
    # check input date dimesions
    shape = np.shape(value)
    if len(shape) > 3:
      raise ValueError('{}-dimension data was given. it must be less than 2'.format(len(shape)))
      
    # create object
    if unit is not None and isinstance(unit, Quantity):
      new = super().__new__(cls, value, unit=unit, **kwargs)
    else:
      new = super().__new__(cls, value, unit=cls._default_yunit, **kwargs)
      
    # set x-axis metadata from xindex
    if xindex is not None:
      # warning about duplicate meta information
      if dx is not None:
        warn('xindex was given to {}, dx will be ignored'.format(cls.__name__))
      if x0 is not None:
        warn('xindex was given to {}, x0 will be ignored'.format(cls.__name__))
      # get unit
      if xunit is None and isinstance(xindex, Quantity):
        xunit = xindex.unit
      elif xunit is None:
        xunit = cls._default_xunit
      # get x0 and dx
      if isinstance(xindex, Quantity):
        new._x0 = xindex[0]
        new._dx = (xindex[1].value-xindex[0].value)*xunit
      else:
        new._x0 = Quantity(xindex[0], xunit)
        new._dx = Quantity(xindex[1]-xindex[0], xunit)
      new.xindex = Quantity(xindex, unit=xunit)
      new.xunit = xunit
    
    # set x-axis metadate from x0 and dx
    else:
      if xunit is None and isinstance(dx, Quantity):
        xunit = dx.unit
      elif xunit is None and isinstance(x0, Quantity):
        xunit = x0.unit
      elif xunit is None:
        xunit = cls._default_xunit
      if dx is not None:
        new.dx = Quantity(float(dx), xunit)
      if x0 is not None:
        new.x0 = Quantity(float(x0), xunit)
      new.xunit = xunit
 
    return new
  
  ##---- Inherent properties --------------------------------
  
  def _set_x_attribute(self, key, value):
    # set the key
    _key = '_{}'.format(key)
    
    # check value quantity
    if not isinstance(value, Quantity):
      try:
        value = Quantity(value, getattr(self, 'xunit'))
      except TypeError:
        value = Quantity(float(value), getattr(self, 'xunit'))
    
    # update new attribute
    try:
      current_attribute = getattr(self, _key)
      if (value is None 
          or not value.unit.is_equivalent(current_attribute.unit)
          or value != current_attribute
          or getattr(self, key) is None):
        delattr(self, _key)
        setattr(self, _key, value)
        
    except AttributeError:
      setattr(self, _key, value)
      
    return value
      
  def _make_index(self, x0, dx, length):
    try:
      xunit = getattr(self, 'xunit')
    except AttributeError:
      xunit = getattr(self, '_default_xunit')
    try:
      index = Quantity(np.arange(x0, x0+(length*dx), dx), unit=xunit)
    except TypeError:
      index = Quantity(np.arange(x0.value, x0.value+(length*dx.value), dx.value), unit=xunit)
    return index
    
  def _set_xindex(self, index):  
    # get length of y
    if np.ndim(self) == 1:
      length = self.shape[0]
    elif np.ndim(self) == 2:
      length = self.shape[1]
      
    try:
      xunit = getattr(self, 'xunit')
    except AttributeError:
      xunit = getattr(self, '_default_xunit')
    
    try:
      if index is not None:
        x0 = index[0]
        dx = index[1]-index[0]
        xindex = self._make_index(x0, dx, length)
        
      else:
        x0 = getattr(self, 'x0')
        dx = getattr(self, 'dx')
        xindex = self._make_index(x0, dx, length)
      
      setattr(self, '_xindex', xindex)      
      
    except AttributeError:
      xindex = self._make_index(0, 1, length)
      setattr(self, '_xindex', xindex)      
    
    return xindex
          
  ##---- properties --------------------------------
  ## x0
  @property
  def x0(self):
    try:
      return self._x0
    except AttributeError:
      self._x0 = Quantity(0, self.xunit)
      return self._x0
  
  @x0.setter
  def x0(self, value):
    self._set_x_attribute('x0', value)
    
  @x0.deleter
  def x0(self):
    try:
      del self._x0
    except AttributeError:
      pass

  ## dx
  @property
  def dx(self):
    try:
      return self._dx
    except AttributeError:
      try:
        self._xindex
      except AttributeError:
        self._dx = Quantity(1, self.xunit)
      else:
        if not self.xindex.regular:
          raise AttributeError('this series index array is not well defined')
        self._dx = self.xindex[1]-self.xindex[0]
      return self._dx
    
  @dx.setter
  def dx(self, value):
    self._set_x_attribute('dx', value)
    
  @dx.deleter
  def dx(self):
    try:
      del self._dx
    except AttributeError:
      pass
    
  ## xindex
  @property
  def xindex(self):
    try:
      return self._xindex
    except AttributeError:
      if np.ndim(self) == 1:
        self._xindex = self._make_index(self.x0, self.dx, self.shape[0])
      elif np.ndim(self) == 2:
        self._xindex = self._make_index(self.x0, self.dx, self.shape[1])
      return self._xindex
  
  @xindex.setter
  def xindex(self, index):
    self._set_xindex(index)
    
  @xindex.deleter
  def xindex(self):
    try:
      del self._xindex
    except AttributeError:
      pass
  
  ##---- mothods -------------------------------- 
  ## add meta data
  @classmethod
  def meta(cls, **kwargs):
    if len(kwargs.keys()) != 0:
      for key, value in kwargs.items():
        setattr(cls, key, value)