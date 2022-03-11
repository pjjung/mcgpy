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

'''frequency : a class to build time-frequency series dataset
'''

import numpy as np
from astropy.units import Quantity
from warnings import warn

from .series import Series

__author__ = 'Phil Jung <pjjung@amcg.kr>'

class FrequencySeries(Series):

  _default_xunit = Quantity(1, 'Hertz')

  def __new__(cls, data, unit=None, f0=None, df=None, frequencies=None, **kwargs):
    '''build time-frequency dataset
    
    Parameters
    ----------
    data : "list", "np.ndarray", "astropy.units.Quantity"
        frequnecy data set
    
    unit : "astropy.units.Quantity", optional
        unit of frequency series,
        if given value is None, it will be set to time-series default unit
    
    f0 : "astropy.units.Quantity", optional
        start point of frequencies,
        if given value is None, it will be set to 0 Hz
    
    df : "astropy.units.Quantity", optional
        interval between frequencies,
        if given valeu is None, it will be set to 1 Hz
    
    frequencies : "astropy.units.Quantity", optional
        x-index of time-frequency series
        if given value is None, it will be built based on f0 and df
    
    Return
    ------
    new : "mcgpy.series.FrequencySeries"
        time-frequency array
        
    Examples
    --------
    >>> from mcgpy.series import FrequencySeries
    >>> import numpy as np
    >>> data = np.random.random(100)
    >>> FrequencySeries(data, f0=0, df=2)
    [0.14420227, 0.91460911, ..., 0.16844983, 0.54762219] 1×10−15T
    >>> FrequencySeries(data, f0=0, df=2).frequencies
    [0, 2, ..., 194, 196, 198] Hz
    '''
    
    if f0 is not None and df is not None:
      kwargs['x0'] = f0
      kwargs['dx'] = df
      new = super().__new__(cls, data, unit=unit, xunit=cls._default_xunit, **kwargs)
      
    if frequencies is not None:
      kwargs['xindex'] = frequencies
      if f0 is not None:
        warn('frequencies was given to {}, f0 will be ignored'.format(cls.__name__))
      if df is not None:
        warn('frequencies was given to {}, df will be ignored'.format(cls.__name__))
        
      f0, df = frequencies[0], frequencies[1]-frequencies[0]
      new = super().__new__(cls, data, unit=unit, xunit=cls._default_xunit, **kwargs)
      new.f0 = f0
      new.df = df
    
    return new
  
  # re-name properties of Series
  
  f0 = property(Series.x0.__get__, Series.x0.__set__, Series.x0.__delete__)
  df = property(Series.dx.__get__, Series.dx.__set__, Series.dx.__delete__)
  frequencies = property(Series.xindex.__get__, Series.xindex.__set__, Series.xindex.__delete__)

  ##---- mothods -------------------------------- 
  
  # at
  def at(self, freq):
    '''get a value at an input frequnecy
    
    Parameters
    ----------
    freq : "int", "float", "astropy.units.Quantity"
        a frequency user want to get the value
        
    Return : "astropy.units.Quantity"
    ------
        the value at an input frequency
    
    Examples
    --------
    >>> from mcgpy.series import FrequencySeries
    >>> import numpy as np
    >>> data = np.random.random(100)
    >>> FrequencySeries(data, f0=0, df=2).at(60)
    0.74917808 1×10−15T
    '''
    
    index = self._find_index(freq)
    f0 = self.frequencies[index]
    new = self[index].view(type(self))
    new.f0 = Quantity(f0, 'Hertz')
    new._unit = self.unit
    
    return self[index] 
  
  # crop
  def crop(self, start, end):
    '''crop a series within an input range
    
    Parameters
    ----------
    start : "int", "float", "astropy.units.Quantity"
    
    end : "int", "float", "astropy.units.Quantity"
    
    Return : "mcgpy.series.FrequencySeries"
    ------
        cropped frequency series
    
    Examples
    --------
    >>> from mcgpy.series import FrequencySeries
    >>> import numpy as np
    >>> data = np.random.random(100)
    >>> FrequencySeries(data, f0=0, df=2).crop(20, 60)
    [0.74373018, 0.073202608, ..., 0.53898833, 0.62487978] 1×10−15T
    '''
    
    start, end = min(self._get_value(start), self._get_value(end)), max(self._get_value(start), self._get_value(end))
    start_index = self._find_index(start)
    end_index = self._find_index(end)
    f0 = self.frequencies[start_index]
    
    new = self[start_index:end_index].view(type(self))
    self._finalize_attribute(new)
    new.f0 = Quantity(f0, 'Hertz')
    new.frequencies = Quantity(np.arange(start, end, self.df.value), 'Hertz')
    new._unit = self.unit
  
    return new
  
  # argmax
  def argmax(self):
    '''get a frequency of a maximum value in a frequency series
    
    Return : "astropy.units.Quantity" 
    ------
        a frequency of the maximum value
    
    Examples
    --------
    >>> from mcgpy.series import FrequencySeries
    >>> import numpy as np
    >>> data = np.random.random(100)
    >>> FrequencySeries(data, f0=0, df=2).argmax()
    110 Hz
    '''
    
    max_index = np.argmax(self.value)
    
    return self.frequencies[max_index]
  
  # argmin
  def argmin(self):
    '''get a frequency of a minimum value in a frequency series
    
    Return : "astropy.units.Quantity"
    ------
        a frequency of the minimum value
    
    Examples
    --------
    >>> from mcgpy.series import FrequencySeries
    >>> import numpy as np
    >>> data = np.random.random(100)
    >>> FrequencySeries(data, f0=0, df=2).argmin()
    196 Hz
    '''
    
    min_index = np.argmin(self.value)

    return self.frequencies[min_index]
  
  ##---- Inherent properties --------------------------------
  def _get_value(self, value):
    if isinstance(value, Quantity):
      return value.value
    else:
      return value
    
  def _find_index(self, epoch):
    epoch = self._get_value(epoch)
    
    FREQUENCIES = self.frequencies.value
    INDEX = np.arange(0, len(self), 1)
    index = INDEX[np.digitize([epoch], FREQUENCIES)[0] - 1]
    
    return index

  def _update_attribute(self, new, key, value):
    _key = '_{}'.format(key)
    try:
      current_attr = getattr(new, _key)
      if (value is None
          or not value.unit.is_equivalent(current_attr.unit)
          or value != current_attr
          or getattr(new, key) is None):
        delattr(new, _key)
        setattr(new, _key, value)

    except AttributeError:
      setattr(new, _key, value)      
  
  def _finalize_attribute(self, new):
    for _key, value in self.__dict__.items():
      key = _key.split('_')[-1]
      self._update_attribute(new, key, value)
  
