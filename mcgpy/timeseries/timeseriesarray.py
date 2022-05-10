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

'''timeseriesarray : the multi-channel time-series array with the matadata 
'''

import os
import numpy as np
from scipy import stats
from astropy.units import (second, Quantity, Unit)
from astropy.table import QTable
from warnings import warn

from ..series import FrequencySeries
from ..channel import (ChannelConfig, ChannelActive)
from ..signal import (bandpass, lowpass, highpass, notch, flattened, rms, fft, asd, psd)
from ..time import tconvert
from ..io._array import Array
from ..io import (KDF, HDF)
from .core import TimeSeriesArrayCore
from .timeseries import TimeSeries

__author__ = 'Phil Jung <pjjung@amcg.kr>'

class TimeSeriesArray(TimeSeriesArrayCore):
  def __new__(cls, source, config=None, positions=None, directions=None, unit=None, t0=None, sample_rate=None, times=None, **kwargs):
    '''make a multi-channel time-series array with metadata
    
    Parameters
    ----------
    source : "str", "list", "np.ndarray", "astropy.units.Quantity", "mcgpy.io.Array"
        it can take multi-type data formats
        
    config : "str", conditional
        if the input source is the KDF file path,
        this parameter is essential
    
    positions : "list", "np.ndarray", "astropy.units.Quantity", optional
        sensor positions
        1) if the input source is the KDF file path and sensor configuration file path is also given,
           this parameter will be ignored
        2) if the input source is the HDF file path,
           this parameter will be ignored
        3) if the input source is user defined data array and will not use numerical classes, "mcgpy.numeric.LeadField" and "mcgpy.numeric.FieldMap",
           this parameter is optional
    
    directions : "list", "np.ndarray", "astropy.units.Quantity", optional
       sensor directions
        1) if the input source is the KDF file path and sensor configuration file path is also given,
           this parameter will be ignored
        2) if the input source is the HDF file path,
           this parameter will be ignored
        3) if the input source is user defined data array and will not use numerical classes, "mcgpy.numeric.LeadField" and "mcgpy.numeric.FieldMap",
           this parameter is optional
           
    unit : "astropy.units.Quantity", optional
        an unit of data
        default unit is femto tesla, 10E-15 T, if the input source is not KDF or HDF5 file path
        
    t0 : "int", "float", "astropy.units.Quantity", optional
        start time of time-series
        default value is 0 s, if the input source is not KDF or HDF5 file path
        
    sample_rate : "int", "float", "astropy.units.Quantity", optional
        signal sample frequency
        default value is 1 Hz, if the input source is not KDF or HDF5 file path
        
    times : "list", "np.ndarray", "astropy.units.Quantity", optional
        time xindex
        default value is made by data size, t0 and sample_rate, if the input source is not KDF or HDF5 file path
    
    Retrun
    ------
        1) if the input source is the path of a KDF or HDF5 file,
           read whole dataset and return it with metadata.
           
        2) if the input source is the data array,
           read a data of given channel number or label, and return it.
           return the time-series array with metadata
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset
    [[136.26814, 156.5814, …, −67.710876, 33.009052], 
     [455.35564, 413.03635, …, 60.093403, 143.03923],
      …, 
     [−1409.2326, −1286.5067,  …, −2374.959, −2407.968], 
     [−1499.7959, −1494.7176,  …,  −1954.3052, −1994.9317]]1×10−15T
    >>> dataset.directions
    array([[1., 0., 0.],
           [1., 0., 0.],
           ...,
           [0., 1., 0.],
           [0., 1., 0.]])
    
    Note
    ----
    this class is designed to apply to numerical classes with a multi-channel time-series of MCG system, though.
    user defined data array can be applied, and use its properties and methods, too.
    '''
   
    if isinstance(source, str):
      # case of KDF file
      if (source is not None and source.split('.')[-1]=='kdf' and os.path.isfile(source)
          and config is not None and config.split('.')[-1]=='ini' and os.path.isfile(config)):
        if positions is not None:
          warn('positions was given to {}, positions will be ignored'.format(cls.__name__))
        if directions is not None:
          warn('directions was given to {}, directions will be ignored'.format(cls.__name__))
        if t0 is not None or sample_rate is not None or times is not None:
          warn('if the path of KDF and config files was given, timeseries arguments (t0, sample_rate, and times) will be ignored'.format(cls.__name__))

        cls._active_channels = ChannelActive(source).get_table()

        for i, row in enumerate(cls._active_channels):
          number = row['number']
          if i == 0:
            positions = ChannelConfig(config).get('positions')[number-1]['positions']
            directions = ChannelConfig(config).get('directions')[number-1]['directions']
            dataset = KDF(source).read(number=number)
            t0 = dataset.t0
            sample_rate = dataset.sample_rate
            cls._biosemi = dataset.biosemi
            cls._info = dataset.info
          else:
            positions = np.vstack((positions, ChannelConfig(config).get('positions')[number-1]['positions']))
            directions = np.vstack((directions, ChannelConfig(config).get('directions')[number-1]['directions']))
            dataset = np.vstack((dataset, KDF(source).read(number=number)))

        new = super().__new__(cls, dataset, positions, directions, unit=unit, t0=t0, sample_rate=sample_rate, **kwargs)


      # case of HDF5 file
      elif (source is not None and source.split('.')[-1]=='hdf5' and os.path.isfile(source)):
        if config is not None:
          warn('configuration path was given to {}, config will be ignored'.format(cls.__name__))
        if positions is not None:
          warn('positions was given to {}, positions will be ignored'.format(cls.__name__))
        if directions is not None:
          warn('directions was given to {}, directions will be ignored'.format(cls.__name__))
        if t0 is not None or sample_rate is not None or times is not None:
          warn('if the path of KDF and config files was given, timeseries arguments (t0, sample_rate, and times) will be ignored'.format(cls.__name__))

        cls._active_channels = ChannelActive(source).get_table()

        for j, row in enumerate(cls._active_channels):
          number = row['number']
          if j == 0:
            dataset = HDF(source).read(number=number)
            positions = np.asarray(dataset.position)
            directions = np.asarray(dataset.direction)
            t0 = dataset.t0
            sample_rate = dataset.sample_rate
            cls._biosemi = dataset.biosemi
            cls._info = dataset.info
          else:
            data = HDF(source).read(number=number)
            positions = np.vstack((positions, data.position))
            directions = np.vstack((directions, data.direction))
            dataset = np.vstack((dataset, data))

        new = super().__new__(cls, dataset, positions, directions, unit=unit, t0=t0, sample_rate=sample_rate, **kwargs) 

    elif isinstance(source, list) or isinstance(source, np.ndarray) or isinstance(source, Quantity) or isinstance(source, mcgpy.io.Array):
      # case of random 2-dimension array
      new = super().__new__(cls, source, positions, directions, unit=unit, t0=t0, sample_rate=sample_rate, times=times, **kwargs)
     
    # other case
    else:
      raise ValueError('invalid arguments were inputted')
    
    return new

  
  ##---- Inherent functions -------------------------------- 
  
  def _get_value(self, value):
    if isinstance(value, Quantity):
      return value.value
    else:
      return value

  def _timestamp_checker(self, timestamp):
    if not self.t0.value <= self._get_value(timestamp) <= self.times[-1].value:
      raise ValueError('invalid timestamp was inputted')
    
  def _find_timeindex(self, epoch):
    epoch = self._get_value(epoch)
    
    TIMES = self.times.value
    INDEX = np.arange(0, self.times.shape[0], 1)
    index = INDEX[np.digitize([epoch], TIMES)[0] - 1]
    
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
      if _key.split('_')[0] == '':
        key = _key[1:]
      else:
        key = _key

      self._update_attribute(new, key, value)
  
  def _offset_guessing(self, data, interval):
    if isinstance(data, Quantity):
      new = data.value - stats.mode(data.value[::interval])[0]
    else:
      new = data - stats.mode(data[::interval])[0]
    return new

  def _convert_infoform(self, info, datetime):
    rearanged_info = ''.join(info.split(' ')[2:4][::-1])
    date = datetime.split(' ')[0].replace('-', '')[2:]
    encoded_info = '{}_{}'.format(rearanged_info, date)
    info_out = {'patient number': info.split(' ')[0],
                'encoded info': encoded_info,
                'opinion': ' '.join(info.split(' ')[4:])}
    return info_out    
  
  def _get_numbers(self):
    try:
      numbers = self._active_channels['number'].value
      
    except AttributeError:
      channel_number = len(self)
      numbers = np.arange(1, 1+channel_number)
    
    return numbers
    
  def _get_labels(self):
    try:
      labels = self._active_channels['label'].value
    except AttributeError:
      channel_number = len(self)
      labels = np.asarray(['label{}'.format(n+1) for n in range(channel_number)])
    
    return labels
  
  def _get_channel_table(self):
    return QTable([self.numbers, self.labels],
                  names=('number', 'label'))
    
  ##---- Properties --------------------------------
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
    if not isinstance(value, Quantity):
      value = Quantity(value, 'Hertz')
    self._update_attribute(self, 'sample_rate', value)
    
  @sample_rate.deleter
  def sample_rate(self):
    try:
      del self._sample_rate
    except AttributeError:
      pass
  
  # duration
  @property
  def duration(self):
    try:
      return self._duration
    except AttributeError:
      self._duration = self.times[-1]-self.times[0]
      return self._duration
    
  @duration.setter
  def duration(self, value):
    self._update_attribute(self, 'duration', value)
  
  @duration.deleter
  def duration(self):
    try:
      del self._duration
    except AttributeError:
      pass
  
  # datetime
  @property
  def datetime(self):
    try:
      return self._datetime
    except AttributeError:
      self._datetime = tconvert(self.t0.value)
      return self._datetime
    
  @datetime.setter
  def datetime(self, value):
    self._update_attribute(self, 'datetime', value)
  
  @datetime.deleter
  def datetime(self):
    try:
      del self._datetime
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
  
  # note; 'info', 'datetime',
  @property
  def note(self):
    try:
      return self._convert_infoform(self._info, self.datetime)
    except AttributeError:
      self._note = None
      return self._note
  
  @note.setter
  def note(self, value):
    self._note = value
    
  @note.deleter
  def note(self):
    try:
      del self._note
    except AttributeError:
      pass
  
  # positions
  @property
  def positions(self):
    return self._positions

    
  @positions.setter
  def positions(self, value):
    self._positions = self._update_attribute(self, 'positions', value)
  
  @positions.deleter
  def positions(self):
    try:
      del self._positions
    except AttributeError:
      pass
  
  # directinons
  @property
  def directions(self):
    return self._directions
  
  @directions.setter
  def directions(self, value):
    self._directions = self._update_attribute(self, 'directions', value)

  @directions.deleter
  def directions(self):
    try:
      del self._directions
    except AttributeError:
      pass
  
  # position
  @property
  def position(self):
    try:
      if np.ndim(self) == 1:
        return self._position
      else:
        pass
    except AttributeError:
      pass
  
  @position.setter
  def position(self, value):
    self._position = self._update_attribute(self, 'position', value)
    
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
      if np.ndim(self) == 1:
        return self._direction
      else:
        pass
    except AttributeError:
      pass
  
  @direction.setter
  def direction(self, value):
    self._direction = self._update_attribute(self, 'direction', value)
    
  @direction.deleter
  def direction(self):
    try:
      del self._direction
    except AttributeError:
      pass
  
  # numbers of active channels
  @property
  def numbers(self):
    try:
      return self._numbers
    except AttributeError:
      self._numbers = self._get_numbers()
      return self._numbers
  
  @numbers.setter
  def numbers(self, value):
    self._numbers = self._update_attribute(self, 'numbers', value)
  
  @numbers.deleter
  def numbers(self):
    try:
      del self._numbers
    except AttributeError:
      pass
  
  # labels of active channels
  @property
  def labels(self):
    try:
      return self._labels
    except AttributeError:
      self._labels = self._get_labels()
      return self._labels
  
  @labels.setter
  def labels(self, value):
    self._labels = self._update_attribute(self, 'labels', value)
  
  @labels.deleter
  def labels(self):
    try:
      del self._labels
    except AttributeError:
      pass

  # number of a channel
  @property
  def number(self):
    try:
      if np.ndim(self) == 1:
        return self._number
      else:
        pass
    except AttributeError:
      pass
    
  @number.setter
  def number(self, value):
    self._number = self._update_attribute(self, 'number', value)
    
  @number.deleter
  def number(self):
    try:
      del self._number
    except AttributeError:
      pass
  
  # label of a channel
  @property
  def label(self):
    try:
      if np.ndim(self) == 1:
        return self._label
      else:
        pass
    except AttributeError:
      pass
    
  @label.setter
  def label(self, value):
    self._label = self._update_attribute(self, 'label', value)
    
  @label.deleter
  def label(self):
    try:
      del self._label
    except AttributeError:
      pass
    
  # number of active channels
  @property
  def channels(self):
    try:
      return self._active_channels
    except AttributeError:
      self._channels = self._get_channel_table()
      return self._channels
  
  
  ##---- Methods --------------------------------
  # at
  def at(self, epoch, **kwargs):  
    '''peak up the value/values at an input time
    
    Parameters
    ----------
    epoch : "int", "float", "astropy.units.Quantity"
        timestamp user wants to get the value
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        1) if the dataset is one-dimensional,
           return the value at the given time
        2) if the dateset is two-dimensional,
           return the values for each channel at the given time
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.at(10)
    [136.26814, 455.35564, ..., −1499.7959, −2495.1458]1×10−15T
    '''
    
    self._timestamp_checker(epoch)
    index = self._find_timeindex(epoch)
    if np.ndim(self) == 1:
      new = self[index]
    
    elif np.ndim(self) == 2:
      new = self[:,index]
      
    self._finalize_attribute(new)
    t0 = self.times[index]
    new.t0 = t0
    new.datetime = tconvert(t0.value)
    
    for key in ['times', 'duration', 'dt']:
      try:
        delattr(new, key)
      except AttributeError:
        pass
      
    return new

  # crop
  def crop(self, start, end, **kwargs):
    '''slice the time-series between start and end times
    
    Parameters
    ----------
    start : "int", "float", "astropy.units.Quantity"
        start timestamp
    
    end : "int", "float", "astropy.units.Quantity"
        end timestamp
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        1) if the dataset is one-dimensional,
           return sliced time-series array
        2) if the dateset is two-dimensional,
           return sliced time-series for each channel array
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.crop(10,12)
    [[136.26814, 156.5814, 177.74105, …, 10.156631, −3.3855438, 5.9247017], 
     [455.35564, 413.03635, 386.79838, …, 394.41586, 352.94294, 360.56042], 
      …, 
     [−1499.7959, −1494.7176, −1477.7899, …, −1535.3441, −1401.6151, −1513.3381], 
     [−2495.1458, −2518.8446, −2456.212, …, −2870.9412, −2869.2484, −2865.0165]]1×10−15T
    '''
    
    self._timestamp_checker(start)
    self._timestamp_checker(end)
    
    start_index = self._find_timeindex(start)
    end_index = self._find_timeindex(end)
    if np.ndim(self) == 1:
      new = self[start_index:end_index]
    
    elif np.ndim(self) == 2:
      new = self[:,start_index:end_index]
      
    self._finalize_attribute(new)
    t0 = self.times[start_index]
    new.t0 = t0
    new.datetime = tconvert(t0.value)
    new._xindex = self.times[start_index:end_index]
    new._duration = Quantity(self.times[end_index]-self.times[start_index], second)
    
    return new

  # bandpass filter
  def bandpass(self, lfreq, hfreq, order=4, flattening=True, **kwargs):
    '''apply the bandpass filter to the dataset
    
    Parameters
    ----------
    series : "list", "np.ndarray", "astropy.units.Quantity"
        ditital signal

    lfreq : "int", "float", "astropy.units.Quantity"
        the low cutoff frequencies 

    hfreq : "int", "float", "astropy.units.Quantity"
        the high cutoff frequencies 

    sample_rate : "int", "float", "astropy.units.Quantity"
        sample rate of ditital signal

    order : "int", optional
        the order of the filter, default value is 4
    
    flattening : Boonlean, optional
        signal flattening option, defaule value is True
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
      filted dataset
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.bandpass(0.1, 200)
    [[5.8798634, 35.303578, 95.930749, …, 72.160133, 27.332395, 18.921922], 
     [19.648239, 113.21599, 288.53974, …, 214.44662, 209.56741, 173.21204], 
     …, 
     [−64.715018, −378.69255, −987.28802, …, −195.79194, −150.83508, −97.942407], 
     [−107.66359, −631.4016, −1649.1429, …, −1785.628, −1803.213, −1788.7173]]1×10−15T
    '''
    
    lfreq, hfreq = self._get_value(min(lfreq, hfreq)), self._get_value(max(lfreq, hfreq))
    filtered_dataset = np.empty(self.shape)
    for i, ch in enumerate(self.value):
      filtered_dataset[i] = bandpass(ch, lfreq=lfreq, hfreq=hfreq, sample_rate=self.sample_rate.value, order=order, flattening=flattening)
    new = filtered_dataset.view(type(self))
    self._finalize_attribute(new)
      
    return new

  # lowpass filter
  def lowpass(self, lfreq, order=2, flattening=True, **kwargs):
    '''apply the lowpass filter to the dataset
    
    Parameters
    ----------
    series : "list", "np.ndarray", "astropy.units.Quantity"
        ditital signal

    freq : "int", "float", "astropy.units.Quantity"
        the cutoff frequencies 

    sample_rate : "int", "float", "astropy.units.Quantity"
        sample rate of ditital signal

    order : "int", optional
        the order of the filter, default value is 2
    
    flattening : Boonlean, optional
        signal flattening option, defaule value is True
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        filted dataset
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.lowpass(300)
    [[27.122792, 96.382285, 158.37537, …, −114.89549, −122.86079, −74.991527], 
     [90.633926, 300.13861, 435.25997, …, 125.62341, 87.47646, 76.55231], 
     …, 
     [−298.51918, −1015.2932, −1538.4497, …, −2075.8569, −2023.2914, −1972.1399], 
     [−496.63348, −1695.4982, −2574.3753, …, −1975.7265, −1958.595, −1906.0884]]1×10−15T
    '''
    
    lfreq = self._get_value(lfreq)
    filtered_dataset = np.empty(self.shape)
    for i, ch in enumerate(self.value):
      filtered_dataset[i] = lowpass(ch, freq=lfreq, sample_rate=self.sample_rate.value, order=order, flattening=flattening)
    new = filtered_dataset.view(type(self))
    self._finalize_attribute(new)
    
    return new
  
  # highpass filter
  def highpass(self, hfreq, order=2, flattening=True, **kwargs):
    '''apply the highpass filter to the dataset
    
    Parameters
    ----------
    series : "list", "np.ndarray", "astropy.units.Quantity"
        ditital signal

    freq : "int", "float", "astropy.units.Quantity"
        the cutoff frequencies 

    sample_rate : "int", "float", "astropy.units.Quantity"
        sample rate of ditital signal

    order : "int", optional
        the order of the filter, default value is 2
    
    flattening : Boonlean, optional
        signal flattening option, defaule value is True
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        filted dataset
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.highpass(1)
    [[135.67819, 154.72616, 174.44649, …, −63.927263, 8.7490505, 108.60693], 
     [453.38425, 407.31395, 377.63813, …, 83.275947, 71.758854, 153.03796], 
     …, 
     [−1493.3028, −1475.2884, −1445.5762, …, 5.3016175, 36.47909, −4.2455184], 
     [−2484.3434, −2486.3819, −2402.3519, …, −128.50984, −103.82009, 51.282091]]1×10−15T
    '''
    
    hfreq = self._get_value(hfreq)
    filtered_dataset = np.empty(self.shape)
    for i, ch in enumerate(self.value):
      filtered_dataset[i] = highpass(ch, freq=hfreq, sample_rate=self.sample_rate.value, order=order, flattening=flattening)
    new = filtered_dataset.view(type(self))
    self._finalize_attribute(new)
    
    return new
      
  # notch filter
  def notch(self, freq, Q=30, flattening=True, **kwargs):
    '''apply the notch/bandstop filter to the dataset
    
    Parameters
    ----------
    series : "list", "np.ndarray", "astropy.units.Quantity"
        ditital signal

    freq : "int", "float", "astropy.units.Quantity"
        the cutoff frequencies 

    sample_rate : "int", "float", "astropy.units.Quantity"
        sample rate of ditital signal

    Q : "int", optional
        the Q-factor of the filter, default value is 30
    
    flattening : Boonlean, optional
        signal flattening option, defaule value is True
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        filted dataset
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.notch(60)
    [[135.4371, 154.08522, 173.6796, …, −134.07926, −57.510631, 44.525834], 
     [452.57862, 405.36713, 375.73626, …, 58.700064, 45.456142, 126.85806], 
     …, 
     [−1490.6493, −1468.6386, −1438.5928, …, −1970.1784, −1950.0809, −2002.2954], 
     [−2479.929, −2475.262, −2390.6521, …, −1948.1221, −1940.4119, −1800.9872]]1×10−15T
    '''
    
    freq = self._get_value(freq)
    filtered_dataset = np.empty(self.shape)
    for i, ch in enumerate(self.value):
      filtered_dataset[i] = notch(ch, freq=freq, sample_rate=self.sample_rate.value, Q=Q)
    new = filtered_dataset.view(type(self))
    self._finalize_attribute(new)
    
    return new
  
  # flattend
  def flattened(self, freq=1, **kwargs):
    '''flattened a wave form by a lowpass filter
    
    Parameters
    ----------
    freq : "int", "float", "astropy.units.Quantity", optional
      the frequency for the lowpass filter, default value is 1 Hz
      
    Return : "mcgpy.timeseries.TimeSeries"
    ------
        (original signal) - (lowpass filtered signal)
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> data = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> data.flattened()
    [[−106.09462, −86.757371, …,−44.093128, −34.719921], [−101.92919, −147.60086, …,  −10.727882, −15.01086], 
    …, 
    [−26.580124, 33.935216,  …, 0.5097395, 0.65614824], 
    [37.148019, 35.133146, …, 22.03233, 31.360074]]1×10−15T
    '''
    if not np.ndim(self) == 2:
      raise TypeError('flattened method only supports a 2-dimensional dataset')
    
    freq = self._get_value(freq)
    filtered_dataset = np.empty(self.shape)
    for i, ch in enumerate(self.value):
      filtered_dataset[i] = flattened(ch, freq, self.sample_rate)
    new = filtered_dataset.view(type(self))
    self._finalize_attribute(new)
    
    return new

  
  # rms
  def rms(self, stride=1, **kwargs):
    '''get the rms dataset by a given stride
    
    Parameters
    ----------
    stride : "int", "float", "astropy.units.Quantity", optional
        sliding step for rms calculation
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        1) if the dataset is one-dimensional,
           return rms series
        2) if the dateset is two-dimensional,
           return rsm series for each channel
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.rms()
    [[397.35058, 475.13264, 335.78015, …, 375.31408, 345.16582, 385.43835],
    [667.53699, 810.86134, 459.06969, …, 595.80191, 563.2746, 617.1745], 
    …, 
    [1497.2229, 1485.2231, 1497.0368, …, 2169.8838, 2085.6369, 2026.235], 
    [2499.4694, 2532.6463, 2630.5988, …, 2015.9665, 666.48291, 1291.5833]]1×10−15T
    '''
    
    stride = self._get_value(stride)
    if np.ndim(self) == 1:
      new = rms(self, self.sample_rate.value, stride).view(type(self))
      self._finalize_attribute(new)
      new.dt = Quantity(stride, second)
      new.sample_rate = Quantity(1/stride, 'Hertz')
      new.times = Quantity(np.arange(self.t0.value, self.t0.value+len(new)//stride, stride), second)
      
      return new
    
    elif np.ndim(self) == 2:
      for i, ch in enumerate(self.value):
        if i == 0:
          dataset = rms(ch, self.sample_rate.value, stride)
        else:
          dataset = np.vstack((dataset, rms(ch, self.sample_rate.value, stride)))
  
      new = dataset.view(type(self))
      self._finalize_attribute(new)
      new.dt = Quantity(stride, second)
      new.sample_rate = Quantity(1/stride, 'Hertz')
      new.times = Quantity(np.arange(self.t0.value, self.t0.value+len(new)//stride, stride), second)
      
      return new
  
  # fft
  def fft(self):
    '''calculate the fast Fourier transform, FFT
    
    Return : "mcgpy.series.FrequencySeries"
    ------
        1) if the dataset is one-dimensional,
           return fft frequency-series
        2) if the dateset is two-dimensional,
           return fft frequency-series for each channel
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.fft()
    [[92.382265, 16.48454, 57.167697, …, 0.05992157, 0.27365534, 0.2273498], 
     [56.252973, 42.362682, 35.193567, …, 0.13228269, 0.017953475, 0.036300067], 
     …,  
     [1741.4278, 104.75867, 48.947051, …, 0.1638588, 0.14912128, 0.073103484], 
     [1630.1735, 103.73168, 145.30199, …, 0.10946647, 0.048501745, 0.073445149]]1×10−15T
    '''
    
    if np.ndim(self) == 1:
      findex, ffty = fft(self, self.sample_rate.value)
      
      return FrequencySeries(ffty, unit=self.unit, frequencies=findex)
      
    elif np.ndim(self) == 2:
      for i, ch in enumerate(self.value):
        if i == 0:
          findex, fftset = fft(ch, self.sample_rate.value)
        else:
          _, ffty = fft(ch, self.sample_rate.value)
          fftset = np.vstack((fftset, ffty))

      return FrequencySeries(fftset, unit=self.unit, frequencies=findex)

  
  # asd
  def asd(self, fftlength=None, overlap=0, window='hann', average='median', **kwargs):
    '''calculate the acceleration spectral density, ASD
    
    Parameters
    ----------
    seglength : "int",  "float", optional
        number of seconds for dividing the time window into equal bins,
        if None type value is given, it will be the size of signal

    overlap : "int", "float", optional
        number of seconds of overlap between FFTs,
        default value is 0

    window : "str"
        Desired window to use. If window is a string or tuple, it is passed to get_window to generate the window values, 
        which are DFT-even by default. See get_window for a list of windows and required parameters. 
        If window is array_like it will be used directly as the window and its length must be nperseg. 
        Defaults to a Hann window.

        See more detailed explanation in "scipy.signal.welch"

    average : { "mean", "median" }, optional
        Method to use when averaging periodograms. 
        Defaults to ‘mean’.

        See more detailed explanation in "scipy.signal.welch"
    
    Return : "mcgpy.series.FrequencySeries"
    ------
        1) if the dataset is one-dimensional,
           return asd frequency-series
        2) if the dateset is two-dimensional,
           return asd frequency-series for each channel
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.asd(2,1)
    [[16.390747, 62.977136, 149.35229, …, 1.8138222, 1.4555211, 0.93069027], 
     [24.143041, 113.88421, 261.50669, …, 1.7955032, 1.8442637, 0.72403336], 
     …, 
     [12.476006, 44.834316, 56.699417, …, 1.6649341, 1.9098386, 1.0112418], 
     [153.54132, 400.77368, 220.70556, …, 1.955279, 1.9509556, 0.80185085]]1×10−15THz1/2
    '''
    
    asd_unit = 1*self.unit/Unit('hertz')**0.5
    if np.ndim(self) == 1:
      findex, asdy = asd(self, self.sample_rate.value, nperseg, overlap, window, average)
      
      return FrequencySeries(asdy, unit=asd_unit, frequencies=findex)
      
    elif np.ndim(self) == 2:
      nperseg = self._get_value(fftlength)
      overlap = self._get_value(overlap)

      for i, ch in enumerate(self.value):
        if i == 0:
          findex, asdset = asd(ch, self.sample_rate.value, nperseg, overlap, window, average)
        else:
          _, asdy = asd(ch, self.sample_rate.value, nperseg, overlap, window, average)
          asdset = np.vstack((asdset, asdy))

      return FrequencySeries(asdset, unit=asd_unit, frequencies=findex)

  
  # psd
  def psd(self, fftlength=None, overlap=0, window='hann', average='median', **kwargs):
    '''calculate the power spectral density, PSD
    
    Parameters
    ----------
    seglength : "int",  "float", optional
        number of seconds for dividing the time window into equal bins,
        if None type value is given, it will be the size of signal

    overlap : "int", "float", optional
        number of seconds of overlap between FFTs,
        default value is 0

    window : "str"
        Desired window to use. If window is a string or tuple, it is passed to get_window to generate the window values, 
        which are DFT-even by default. See get_window for a list of windows and required parameters. 
        If window is array_like it will be used directly as the window and its length must be nperseg. 
        Defaults to a Hann window.

        See more detailed explanation in "scipy.signal.welch"

    average : { "mean", "median" }, optional
        Method to use when averaging periodograms. 
        Defaults to ‘mean’.

        See more detailed explanation in "scipy.signal.welch"
    
    Return : "mcgpy.series.FrequencySeries"
    ------
        1) if the dataset is one-dimensional,
           return psd frequency-series
        2) if the dateset is two-dimensional,
           return psd frequency-series for each channel
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.psd(2,1)
    [[16.390747, 62.977136, 149.35229, …, 1.8138222, 1.4555211, 0.93069027], 
     [582.88645, 12969.614, 68385.748, …, 3.2238317, 3.4013085, 0.5242243], 
     …, 
     [155.65072, 2010.1159, 3214.8239, …, 2.7720054, 3.6474833, 1.02261], 
     [23574.937, 160619.55, 48710.946, …, 3.823116, 3.8062277, 0.64296479]]1×10−30T2Hz
    '''
    
    psd_unit = 1*self.unit**2/Unit('hertz')
    if np.ndim(self) == 1:
      findex, asdy = asd(self, self.sample_rate.value, nperseg, overlap, window, average)
      
      return FrequencySeries(asdy, unit=self.unit, frequencies=findex)
      
    elif np.ndim(self) == 2:
      nperseg = self._get_value(fftlength)
      overlap = self._get_value(overlap)

      for i, ch in enumerate(self.value):
        if i == 0:
          findex, asdset = asd(ch, self.sample_rate.value, nperseg, overlap, window, average)
        else:
          _, asdy = psd(ch, self.sample_rate.value, nperseg, overlap, window, average)
          asdset = np.vstack((asdset, asdy))

      return FrequencySeries(asdset, unit=psd_unit, frequencies=findex)

  
  # offset correction
  def offset_correction(self, interval=2, **kwargs):
    '''offset correction by signal mode value
    
    Parameters
    ----------
    interval : "int"
        number of seconds for dividing the time-series
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        offset corrected dataset for each channel based on the signal mode value
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.offset_correction()
    [[165.89165, 186.20491, 207.36456, …, −110.87656, −38.087368, 62.632561], 
     [236.98807, 194.66877, 168.43081, …, −148.11754, −158.27417, −75.32835], 
     …, 
     [514.60266, 519.68098, 536.6087, …, 28.777122, 60.093403, 19.466877], 
     [55.015087, 31.31628, 93.948841, …, 598.39487, 620.40091, 773.59676]]1×10−15T

    Note
    ----
    "scipy.stats.mode" is utilized to match the baseline of multi-channels, in which the mode is the modal (most common) value in the passed array.
    '''
    
    if np.ndim(self) == 1:
      adjusted = self._offset_guessing(self, interval)
      new = adjusted.view(type(self))
      self._finalize_attribute(new)

      return new  
    
    elif np.ndim(self) == 2:
      dataset = np.empty(self.shape)
      for i, ch in enumerate(self.value):
        dataset[i] = self._offset_guessing(ch, interval)
      new = dataset.view(type(self))
      self._finalize_attribute(new)

      return new
      
  # offset correction at
  def offset_correction_at(self, epoch, **kwargs):
    '''offset correction by the value at the given timestamp,
       each signal offset will be subtracted from the value at the given timestamp
    
    Parameters
    ----------
    epoch : "int", "float", "astropy.units.Quantity"
        timestamp user wants to get the value
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        offset corrected dataset for each channel based on the value of the input timestamp
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.offset_correction_at(10)
    [[165.04526, 185.35852, 206.51817, …, −111.72295, −38.933754, 61.786175], 
     [27.084351, −15.234947, −41.472912, …, −358.02126, −368.17789, −285.23207], 
     …, 
     [−11.849403, −6.7710876, 10.156631, …, −497.67494, −466.35866, −506.98519], 
     [323.31944, 299.62063, 362.25319, …, 866.69922, 888.70525, 1041.9011]]1×10−15T
    '''
    
    index = self._find_timeindex(epoch)
    if np.ndim(self) == 1:
      adjusted = self - self[index]
      new = adjusted.view(type(self))
      self._finalize_attribute(new)

      return new
    
    elif np.ndim(self) == 2:
      dataset = np.empty(self.shape)
      for i, ch in enumerate(self.value):
        dataset[i] = ch - ch[index]
      new = dataset.view(type(self))
      self._finalize_attribute(new)

      return new
             
  # to_rms
  def to_rms(self):
    '''calculate the rms for all channels
    
    Raises
    ------
    TypeError
        if the dataset was one-dimensional
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        rms time-series, 1D-array
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.to_rms()
    [1881.8758, 1874.3042, …, 1929.9437, 1915.6712]1×10−15T
    '''
    
    if np.ndim(self) == 2:
      dataset = np.empty(0)
      for column in self.value.T:
        dataset = np.append(dataset, np.sqrt(np.mean(column**2)))
      new = dataset.view(type(self))
      self._finalize_attribute(new)
      del new.positions
      del new.directions
      return new
    else:
      raise TypeError('to_rms method only supports a 2-dimensional dataset')
  
  # to_avg
  def to_avg(self):
    '''calculate an average of channel signals
    
    Raises
    ------
    TypeError
        if the dataset was one-dimensional
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        an average of channel signals, 1D-array
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.to_avg()
    [−308.02403, −316.00424, …, −549.95943, −541.59633]1×10−15T
    '''
    
    if np.ndim(self) == 2:
      dataset = np.empty(0)
      for column in self.value.T:
        dataset = np.append(dataset, np.mean(column))
      new = dataset.view(type(self))
      self._finalize_attribute(new)
      del new.positions
      del new.directions
      return new
    else:
      raise TypeError('to_avg method only supports a 2-dimensional dataset')
  
  # area
  def area(self, start, end):
    '''calculate the area between start and end timestamps
    
    Parameters
    ----------
    start : "int", "float", "astropy.units.Quantity"
        start timestamp
    
    end : "int", "float", "astropy.units.Quantity"
        end timestamp
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        1) if the dataset is one-dimensional,
           return the area of signal between start and end timestamps
        2) if the dateset is two-dimensional,
           return the area of signal between start and end timestamps for each channel
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.area(10,12)
    [0.24546295, 0.46202301, ..., 1.409447, 2.6042676](𝑈𝑛𝑖𝑡𝑛𝑜𝑡𝑖𝑛𝑖𝑡𝑖𝑎𝑙𝑖𝑠𝑒𝑑)
    '''
    
    start_index, end_index = self._find_timeindex(min(start, end)), self._find_timeindex(max(start, end))
    dt = self.dt.value
    if np.ndim(self) == 1:
      source = self[start_index:end_index].value
      area = np.multiply(np.mean(abs(source)), dt)
      new = area.view(type(self))
      t0 = self.times[start_index]
      new.t0 = t0
      new.datetime = tconvert(t0.value)

      return new
    
    elif np.ndim(self) == 2:
      source = self[:,start_index:end_index].value
      dataset = np.empty(0)
      for ch in source:
        dataset = np.append(dataset, np.multiply(np.mean(abs(ch)), dt))
      new = dataset.view(type(self))
      t0 = self.times[start_index]
      new.t0 = t0
      new.datetime = tconvert(t0.value)

      return new
  
  # integral
  def integral(self, start, end):
    '''calculate the integrated area between start and end timestamps
    
    Parameters
    ----------
    start : "int", "float", "astropy.units.Quantity"
        start timestamp
    
    end : "int", "float", "astropy.units.Quantity"
        end timestamp
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        1) if the dataset is one-dimensional,
           return the integrated area between start and end timestamps
        2) if the dateset is two-dimensional,
           return the integrated area between start and end timestamps for each channel
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.intergral(10,12)
    [0.057181275, 0.18835077, ..., −1.409359, −2.5957822](𝑈𝑛𝑖𝑡𝑛𝑜𝑡𝑖𝑛𝑖𝑡𝑖𝑎𝑙𝑖𝑠𝑒𝑑)
    '''
    
    start_index, end_index = self._find_timeindex(min(start, end)), self._find_timeindex(max(start, end))
    dt = self.dt.value
    if np.ndim(self) == 1:
      source = self[start_index:end_index].value
      area = np.multiply(np.mean(source), dt)
      new = area.view(type(self))
      t0 = self.times[start_index]
      new.t0 = t0
      new.datetime = tconvert(t0.value)

      return new
    
    elif np.ndim(self) == 2:
      source = self[:,start_index:end_index].value
      dataset = np.empty(0)
      for ch in source:
        dataset = np.append(dataset, np.multiply(np.mean(ch), dt))
      new = dataset.view(type(self))
      t0 = self.times[start_index]
      new.t0 = t0
      new.datetime = tconvert(t0.value)

      return new
  
  # read
  def read(self, number=None, label=None, **kwargs):
    '''read one channel data from the dataset
    
    Parameters
    ----------
    number : "int", conditional
        number of a channel, while label parameter is None
    
    label : "str", conditional
        label of a channel, while number parameter is None
    
    Return : "mcgpy.timeseries.TimeSeries"
    ------
        a single channel time-series data
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.read(number=1)
    [136.26814, 156.5814, …, −67.710876, 33.009052]1×10−15T
    '''
    
    if number is not None and label is None:
      index = np.argwhere(self.channels['number'] == int(number))[0][0]
      label = self.channels['label'][index]

    elif number is None and lable is not None:
      index = np.argwhere(self.channels['label'] == str(label))[0][0]
      number = self.channels['number'][index]
    
    elif number is not None and label is not None:
      raise TypeError('read() takses 1 argument, number or label, but 2 were given')
    
    else:
      raise TypeError('read() takses 1 argument, number or label, but 0 were given')
  
    new = TimeSeries(source=self[index], number=number, label=label, times=self.times)
    new.position = self.positions[index]
    new.direction = self.directions[index]
    new.datetime = self.datetime
    new.biosemi = self.biosemi
    new.note = self.note

    return new
  
  # exclude
  def exclude(self, numbers=None, labels=None, **kwargs):
    '''except the channel data from the dataset
    
    Parameters
    ----------
    numbers : "list", "tuple", "np.ndarray", conditional
        the number list of what user wants to remove channels from the dataset
    
    labels : "list", "tuple", "np.ndarray", conditional
        the label list of what user wants to remove channels from the dataset
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    ------
        the dataset except for the given channel list
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> dataset.exclude(numbers=(1,2,3,4))
    [[485.82554, 424.03936, 330.93691, …, 534.91592, 451.9701, 475.66891], 
     [214.13565, 215.82842, 265.76519, …, 275.92182, 276.76821, 246.29831], 
     …, 
     [−1499.7959, −1494.7176, −1477.7899, …, −1985.6215, −1954.3052, −1994.9317], 
     [−2495.1458, −2518.8446, −2456.212, …, −1951.766, −1929.76, −1776.5641]]1×10−15T
    '''
    
    exclude_indexes = list()
    if numbers is not None and labels is None:
      if not (isinstance(numbers, list) or isinstance(numbers, tuple) or isinstance(numbers, np.ndarray)):
        raise AttributeError('exclude() takse list, tuple, or numpy array type argument')
      
      for number in numbers:
        exclude_indexes.append(np.argwhere(self.numbers == number)[0][0])
        
    elif numbers is None and labels is not None:
      if not (isinstance(labels, list) or isinstance(numbers, tuple) or isinstance(numbers, np.ndarray)):
        raise AttributeError('exclude() takse list, tuple, or numpy array type argument')

      for label in labels:
        exclude_indexes.append(np.argwhere(self.labels == label)[0][0])
        
    new = np.delete(self, exclude_indexes, axis=0).view(type(self))
    self._finalize_attribute(new)
    new._numbers = np.delete(self.numbers, exclude_indexes, axis=0)
    new._labels = np.delete(self.labels, exclude_indexes, axis=0)
    new._positions = np.delete(self.positions, exclude_indexes, axis=0)
    new._directions = np.delete(self.directions, exclude_indexes, axis=0)

    return new
  
  # argmax
  def argmax(self):
    '''find the epoch of the maximum value
    
    Return : 
    ------
      if the dataset is one-dimensional, return will be a timestamp of the maximum value : "astropy.table.Quantity"
    
      if the dataset is two-dimensional, return will be timestamps of the maximum values for each channel : "astropy.table.Quantity" in "list"
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> data = TimeSeriesArray("~/test/raw/file/path.hdf5").to_rms()
    >>> data.max()
    4480.30971×10−15T
    >>> data.argmax()
    11.3447265625 s
    '''
    if np.ndim(self) == 1:
      return self.times[np.argmax(self.value)]
    
    elif np.ndim(self) == 2:
      out = list()
      for ch in self.value:
        out.append(self.times[np.argmax(ch)])
      return out
  
  # argmin
  def argmin(self):
    '''find the epoch of the minimum value
    
    Return :
    ------
      if the dataset is one-dimensional, return will be a timestamp of the minimum value : "astropy.table.Quantity"
    
      if the dataset is two-dimensional, return will be timestamps of the minimum values for each channel : "astropy.table.Quantity" in "list"
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeriesArray
    >>> data = TimeSeriesArray("~/test/raw/file/path.hdf5").to_rms()
    >>> data.min()
    53.7786021×10−15T
    >>> data.argmin()
    10 s
    '''
    if np.ndim(self) == 1:
      return self.times[np.argmin(self.value)]
    
    elif np.ndim(self) == 2:
      out = list()
      for ch in self.value:
        out.append(self.times[np.argmin(ch)])
      return out

