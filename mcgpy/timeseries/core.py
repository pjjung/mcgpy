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

'''core : the core part of building time-series and time-series arrary classes
'''

import numpy as np
from scipy import stats
from astropy import units as u
from astropy.units import (second, Quantity, Unit)
from warnings import warn

from ..series import (Series, FrequencySeries)
from ..time import tconvert
from ..channel import (ChannelConfig, ChannelActive)
from ..signal import (bandpass, lowpass, highpass, notch, rms, fft, asd, psd)
from ..io._array import Array

__author__ = 'Phil Jung <pjjung@amcg.kr>'
__all__ = ['TimeSeriesCore', 'TimeSeriesArrayCore']


###---- TimeSeriesCore Class ---------------------------------------------------------------------------------------------------------------##   

class TimeSeriesCore(Series):
  
  _genetic_attributes = ['biosemi', 'info', 'datetime', 'duration', 'number', 'label', 'position', 'direction']
  
  def __new__(cls, data, unit=None, t0=None, sample_rate=None, times=None, *args, **kwargs):
    '''basic time-series array builder
    
    Parameters
    ----------
    data : "list", "np.ndarray", "astropy.units.Quantity"
        a single-channel time-series data
    
    unit : "astropy.units.Quantity", optional
        an unit of data
    
    t0 : "int", "float", "astropy.units.Quantity", optional
        start time of times, timestamp
    
    sample_rate : "int", "float", "astropy.units.Quantity", optional
        signal sample frequency
    
    times : "list", "np.ndarray", "astropy.units.Quantity", optional
        time xindex
    
    Return
    ------
    new : "mcgpy.timeseries.TimeSeriesCore"
        the single-channel time-series array with the metadata as class properties
    
    Note
    ----
    this class is made to establish a time-series quantity array from the raw dataset.
    elements in the "genetic_attributes" list are the key of attributes contained in the metadata of raw dataset.
    '''
    
    if t0 is not None:
      kwargs['x0'] = t0
    elif t0 is None and isinstance(data, Array):
      try:
        kwargs['x0'] = getattr(data, 't0')
      except AttributeError:
        pass
    
    if sample_rate is not None:
      kwargs['dx'] = 1/sample_rate
    elif sample_rate is None and isinstance(data, Array):
      try:
        sample_rate = getattr(data, 'sample_rate')
        kwargs['dx'] = 1/sample_rate
      except AttributeError:
        pass
    elif sample_rate is None and times is not None:
      if isinstance(times, Quantity):
        sample_rate = 1/(times[1].value-times[0].value)
      else:
        sample_rate = 1/(times[1]-times[0])
      
    if times is not None:
      kwargs['xindex'] = times
    
    new = super().__new__(cls, data, unit=unit, xunit=second, **kwargs)
    
    if isinstance(data, Array):
      for attr in cls._genetic_attributes:
        try:
          key = '_{}'.format(attr)
          value = getattr(data, attr)
          setattr(new, key, value)
        except AttributeError:
          setattr(new, key, None)
    
    if sample_rate:
      new._sample_rate = Quantity(sample_rate, 'Hertz')
    else:
      new._sample_rate = Quantity(1, 'Hertz')
    
    return new

    
  # re-name properties of Series
  t0 = Series.x0
  dt = Series.dx
  times = Series.xindex
  
  ##---- Inherent functions --------------------------------  
  
  def _get_duration(self, sample_rate):
    if isinstance(sample_rate, Quantity):
      sample_rate = sample_rate.value
    
    return Quantity(len(self)/sample_rate, second)
  
  def _set_sample_rate(self, key, value):
    _key = '_{}'.format(key)

    if not isinstance(value, Quantity):
      try:
        value = Quantity(value, 'Hertz')
      except TypeError:
        value = Quantity(float(value), 'Hertz')
        
    try:
      current_sample_rate = getattr(self, _key)
      if (value is None
          or not value.unit.is_equivalent(current_sample_rate.unit)
          or value != current_sample_rate
          or getattr(self, key) is None):
        delattr(self, _key)
        setattr(self, _key, value)
    except AttributeError:
      setattr(self, _key, value)
      
    return value
  
  def _convert_infoform(self, info, datetime):
    rearanged_info = ''.join(info.split(' ')[2:4][::-1])
    date = datetime.split(' ')[0].replace('-', '')[2:]
    encoded_info = '{}_{}'.format(rearanged_info, date)
    info_out = {'patient number': info.split(' ')[0],
                'encoded info': encoded_info,
                'opinion': ' '.join(info.split(' ')[4:])}
    return info_out
  
  ##---- Properties --------------------------------
  
  # duration
  @property
  def duration(self):
    try:
      if not isinstance(self._duration, Quantity):
        return Quantity(self._duration, second)
      else:
        return self._duration
    except AttributeError:
      self._duration = self._get_duration(self._sample_rate)
      return self._duration
  
  @duration.setter
  def duration(self, value):
    self.meta(duration=value)
  
  @duration.deleter
  def duration(self):
    try:
      del self._duration
    except AttributeError:
      pass
  
  # sample rate
  @property
  def sample_rate(self):
    try:
      return self._sample_rate
    except AttributeError:
      self._sample_rate = Quantity(1, 'Hertz')
      return self._sample_rate
    
  @sample_rate.setter
  def sample_rate(self, value):
    self._set_sample_rate('sample_rate', value)
    
  @sample_rate.deleter
  def sample_rate(self):
    try:
      del self._sample_rate
    except AttributeError:
      pass
  
  # note; 'info', 'datetime',
  @property
  def note(self):
    try:
      return self._note
    except AttributeError:
      try:
        self._note = self._convert_infoform(self._info, self._datetime)
        return self._note
      except AttributeError:
        return None
  
  @note.setter
  def note(self, value):
    self._note = value
    
  @note.deleter
  def note(self):
    try:
      del self._note
    except AttributeError:
      pass
  
  # biosemi
  @property
  def biosemi(self):
    try:
      return self._biosemi
    except AttributeError:
      self._biosemi = None
      return self._biosemi
    
  @biosemi.setter
  def biosemi(self, value):
    self._biosemi = value
    
  @biosemi.deleter
  def biosemi(self):
    try:
      del self._biosemi
    except AttributeError:
      pass
  
  # datetime
  @property
  def datetime(self):
    try:
      return self._datetime
    except AttributeError:
      self._datetime = tconvert(self.t0)
      return self._datetime
  
  @datetime.setter
  def datetime(self, value):
    self._datetime = value
    
  @datetime.deleter
  def datetime(self):
    try:
      del self._datetime
    except AttributeError:
      pass
  
  # number
  @property
  def number(self):
    try:
      return self._number
    except AttributeError:
      self._numner = None
      return self._number
  
  @number.setter
  def number(self, value):
    self._number = int(value)
    
  @number.deleter
  def number(self):
    try:
      del self._number
    except AttributeError:
      pass
  
  # label
  @property
  def label(self):
    try:
      return self._label
    except AttributeError:
      self._label = None
      return self._label
    
  @label.setter
  def label(self, value):
    self._label = str(value)
    
  @label.deleter
  def label(self):
    try:
      del self._label
    except AttributeError:
      pass
  
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
    self._position = value
    
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
    self._direction = value
    
  @direction.deleter
  def direction(self):
    try:
      del self._direction
    except AttributeError:
      pass

###---- TimeSeriesArrayCore Class ---------------------------------------------------------------------------------------------------------------##   
class TimeSeriesArrayCore(Series):
  
  _default_yunit = Unit('tesla')*10**-15 #femto tesla [fT]

  def __new__(cls, dataset, positions, directions, unit=None, t0=None, sample_rate=None, times=None, *args, **kwargs):
    '''basic multi-channel time-series array builder
    
    Parameters
    ----------
    dataset : "list", "np.ndarray", "astropy.units.Quantity"
        a multi-channel dataset
    
    positions : "list", "np.ndarray", "astropy.units.Quantity"
        the list contained sensor's position coordinates on the sensor plane
    
    directions : "list", "np.ndarray", "astropy.units.Quantity"
        the list contained sensor's directions on the sensor plane
    
    unit : "astropy.units.Quantity", optional
        an unit of data
    
    t0 : "int", "float", "astropy.units.Quantity", optional
        start time of times, timestamp
    
    sample_rate : "int", "float", "astropy.units.Quantity", optional
        signal sample frequency
    
    times : "list", "np.ndarray", "astropy.units.Quantity", optional
        time xindex
    
    Return
    ------
    new : "mcgpy.timeseries.TimeSeriesArrayCore"
        multi-channel time-series array,
        each row is a channel data, and columns are time-series data points
    '''
    
    if not len(dataset) == len(positions) == len(directions):
      raise TypeError('the number of row lines given arguments must be same: ({}), ({}), ({})'.format(len(dataset), len(positions), len(directions)))
    else:
      if len(positions[0]) != 3:
        raise TypeError('the element in positions must consist of (x, y, z)')
      if len(directions[0]) != 3:
        raise TypeError('the element in directions must consist of (x, y, z)')
      
    if t0 is not None:
      kwargs['x0'] = t0
    elif t0 is None:
      try:
        kwargs['x0'] = getattr(dataset, 't0')
      except AttributeError:
        pass
    
    if sample_rate is not None:
      kwargs['dx'] = 1/sample_rate
    elif sample_rate is None:
      try:
        sample_rate = getattr(dataset, 'sample_rate')
        kwargs['dx'] = 1/sample_rate
      except AttributeError:
        pass
      
    if times is not None:
      kwargs['xindex'] = times
      
    if unit is None:
      unit = cls._default_yunit
    
    new = super().__new__(cls, dataset, unit=unit, xunit=second, **kwargs)
    
    new._positions = np.asarray(positions)
    new._directions = np.asarray(directions)
    if sample_rate:
      new._sample_rate = Quantity(sample_rate, 'Hertz')
    else:
      new._sample_rate = Quantity(1, 'Hertz')
      
    return new
  
  t0 = Series.x0
  dt = Series.dx
  times = Series.xindex
  
