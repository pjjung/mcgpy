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

'''timeseries : the single-channel time-series array with the metadata 
'''

import os
import numpy as np
from scipy.signal import find_peaks
from astropy.units import (Quantity, second)
from astropy import units as u

from ..signal import (bandpass, lowpass, highpass, notch, flattened, rms, fft, asd, psd)
from ..series import FrequencySeries
from ..io import (KDF, HDF)
from ..time import tconvert
from .core import TimeSeriesCore 

__author__ = 'Phil Jung <pjjung@amcg.kr>'

class TimeSeries(TimeSeriesCore):
  def __new__(cls, source, number=None, label=None, unit=None, t0=None, sample_rate=None, times=None, *args, **kwargs):
    '''make a single-channel time-series array with metadata
    
    Parameters
    ----------
    source : "str", "list", "np.ndarray", "astropy.units.Quantity", "mcgpy.io.Array"
        it can take multi-type data formats
        
    number : "int", conditional
        channel's number
        1) if the input source is the path of a raw file and the label is None value,
           this parameter is essential for reading a channel data
        2) if the input source is the data array,
           this parameter is optional
    
    label : "str", conditional
        channel's label
        1) if the input source is the path of a raw file and the number is None value,
           this parameter is essential for reading a channel data
        2) if the input source is the data array,
           this parameter is optional
    
    unit : "astropy.units.Quantity", optional
        an unit of data
        default unit is femto tesla, 10E-15 T, if the input source is not a raw file path
    
    t0 : "int", "float", "astropy.units.Quantity", optional
        start time of time-series
        default value is 0 s, if the input source is not a raw file path
    
    sample_rate : "int", "float", "astropy.units.Quantity", optional
        signal sample frequency
        default value is 1 Hz, if the input source is not a rwa file path
    
    times : "list", "np.ndarray", "astropy.units.Quantity", optional
        time xindex
        default value is made by data size, t0 and sample_rate, if the input source is not a raw file path
    
    Return : "mcgpy.timeseries.TimeSeries"
    ------
        1) if the input source is the path of a raw file,
           read a data of given channel number or label, and return it.
           in this case, a number or label parameter is essential
        2) if the input source is the data array,
           return the time-series array by given parameters
           
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> import numpy as np
    >>> source = np.random.random(100)
    >>> data = TimeSeries(source, sample_rate=10)
    >>> print(data)
    [0.82405757 0.34912628 ... 0.35523488 0.9324402 ] 1e-15 T
    >>> print(data.times)
    [0.  0.1 ... 9.8 9.9] s
    >>>
    >>> path = "~/test/raw/file/path.hdf5"
    >>> data = TimeSeries(path, number=1)
    >>> print(data)
    [ 136.26813889  156.58140182  ...  -67.71087646  33.00905228] 1e-15 T

    Note
    ----
    this class is designed to deal with a single-channel time-series of MCG system, though.
    user defined data array can be applied, and use its properties and methods
    '''
    
    if isinstance(source, str) and os.path.isfile(source):
      if source.split('.')[-1] == 'kdf':
        source = KDF(source).read(number, label)
      elif source.split('.')[-1] == 'hdf5':
        source = HDF(source).read(number, label)
    elif isinstance(source, Quantity):
      unit = source.unit
        
    new = super().__new__(cls, data=source, unit=unit, t0=t0, sample_rate=sample_rate, times=times, *args, **kwargs)
    new._number = number
    new._label = label
    
    return new

  
  ##---- Inherent functions --------------------------------  
  def _get_value(self, value):
    if isinstance(value, Quantity):
      return value.value
    else:
      return value
  
  def _find_index(self, epoch):
    epoch = self._get_value(epoch)
    
    TIMES = self.times.value
    INDEX = np.arange(0, self.times.shape[0], 1)
    index = INDEX[np.digitize([epoch], TIMES)[0] - 1]
    
    return index

  def _timestamp_checker(self, timestamp):
    if not self.t0.value <= self._get_value(timestamp) <= self.times[-1].value:
      raise ValueError('invalid timestamp was inputted')
  
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

  def _filter(self, filter_type, lfreq=None, hfreq=None, notchfreq=None, flattening=True, **kwargs):
    if (filter_type == 'bandpass' 
        and lfreq is not None 
        and hfreq is not None):
      _lfreq, _hfreq = self._get_value(min(lfreq, hfreq)), self._get_value(max(lfreq, hfreq))

      filtered_data = bandpass(self.value, _lfreq, _hfreq, self._sample_rate.value, kwargs['order'], flattening)
 
    elif (filter_type == 'lowpass' and lfreq is not None):
      _lfreq = self._get_value(lfreq)
      
      filtered_data = lowpass(self.value, _lfreq, self._sample_rate.value, kwargs['order'], flattening)
    
    elif (filter_type == 'highpass' and hfreq is not None):
      _hfreq = self._get_value(hfreq)
      
      filtered_data = highpass(self.value, _hfreq, self._sample_rate.value, kwargs['order'], flattening)
    
    elif (filter_type == 'notch' and notchfreq is not None):
      _notchfreq = self._get_value(notchfreq)
      
      filtered_data = notch(self.value, _notchfreq, self.sample_rate.value, kwargs['Q'], flattening)
      
    else:
      raise ValueError('invalid arguments were inputted')

    new = filtered_data.view(type(self))
    self._finalize_attribute(new)
    new._unit = self.unit
    
    return new
  
  ##---- Methods -------------------------------- 

  # at
  def at(self, epoch):
    '''peak up the value at an input time
    
    Parameters
    ----------
    epoch : "int", "float", "astropy.units.Quantity"
        timestamp user wants to get the value
    
    Retrun : "mcgpy.timeseries.TimeSeries"
    ------
        the valeu at an input timestamp
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.at(10)
    136.268141×10−15T
    '''
    
    self._timestamp_checker(epoch)
    
    epoch = self._get_value(epoch)
    index = self._find_index(epoch)
    
    t0 = self.times[index]
    new = self[index].view(type(self))
    new.datetime = tconvert(epoch)
    new.t0 = self.times[index]
    new._unit = self.unit
    
    return new 

  # crop
  def crop(self, start, end):
    '''slice the time-series between start and end times
    
    Parameters
    ----------
    start : "int", "float", "astropy.units.Quantity"
        start timestamp
    
    end : "int", "float", "astropy.units.Quantity"
        end timestamp
    
    Retrun : "mcgpy.timeseries.TimeSeries"
    ------
        sliced time-series array
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.crop(10,12)
    [136.26814, 156.5814, …, −256.45494, −223.44589]1×10−15T
    '''
    
    self._timestamp_checker(start)
    self._timestamp_checker(end)
    
    start, end = min(self._get_value(start), self._get_value(end)), max(self._get_value(start), self._get_value(end))
    start_index = self._find_index(start)
    end_index = self._find_index(end)
    
    new = self[start_index:end_index].view(type(self))
    self._finalize_attribute(new)
    new.t0 = self.times[start_index]
    new.datetime = tconvert(start)
    new.duration = Quantity(end-start, second)
    new.times = self.times[start_index:end_index]
    new._unit = self.unit
  
    return new
  
  # rms
  def rms(self, stride=1):
    '''get the rms series by a given stride
    
    Parameters
    ----------
    stride : "int", "float", "astropy.units.Quantity", optional
        sliding step for rms calculation
    
    Retrun : "mcgpy.timeseries.TimeSeries"
    ------
        rms series
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.rms()
    [397.35058, 475.13264, ..., 345.16582, 385.43835]1×10−15T
    
    '''
    
    stride = self._get_value(stride)
    new = rms(self.value, self.sample_rate.value, stride).view(type(self))
    
    new.t0 = self.t0
    new.dt = Quantity(stride, second)
    new.sample_rate = Quantity(1/stride, 'Hertz')
    new.times = Quantity(np.arange(self.t0.value, self.t0.value+len(new)//stride, stride), second)
    new._unit = self.unit
    
    return new
    
  # bandpass filter
  def bandpass(self, lfreq, hfreq, order=4, flattening=True):
    '''apply the bandpass filter to the data
    
    Prameters
    ---------
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

    Retrun : "mcgpy.timeseries.TimeSeries"
    ------
        filted series
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.bandpass(0.1, 200)
    [5.8798634, 35.303578, …, 27.332395, 18.921922]1×10−15T
    '''
    
    return self._filter(filter_type='bandpass', lfreq=lfreq, hfreq=hfreq, order=order, flattening=flattening)

  # lowpass filter
  def lowpass(self, lfreq, order=2, flattening=True):
    '''apply the lowpass filter to the data
    
    Prameters
    ---------
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

    Retrun : "mcgpy.timeseries.TimeSeries"
    ------
        filted series
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.lowpass(300)
    [51.327193, 145.35014,  …, −111.09751, −31.626277]1×10−15T
    '''
    
    return self._filter(filter_type='lowpass', lfreq=lfreq, order=order, flattening=flattening)
  
  # highpass filter
  def highpass(self, hfreq, order=2, flattening=True):
    '''apply the highpass filter to the data
    
    Prameters
    ---------
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

    Retrun : "mcgpy.timeseries.TimeSeries"
    ------
        filted series
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.highpass(1)
    [135.67819, 154.72616, …, 8.7490505, 108.60693]1×10−15T
    '''
    
    return self._filter(filter_type='highpass', hfreq=hfreq, order=order, flattening=flattening)
      
  # notch filter
  def notch(self, freq, Q=30, flattening=True):
    '''apply the notch/bandstop filter to the data
    
    Prameters
    ---------
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

    Retrun : "mcgpy.timeseries.TimeSeries"
    ------
        filted series
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.notch(60)
    [135.4371, 154.08522,  …, −57.510631, 44.525834]1×10−15T
    '''
    return self._filter(filter_type='notch', notchfreq=freq, Q=Q, flattening=flattening)

  # flattened
  def flattened(self, freq=1, **kwargs):
    '''flatten a wave form by a lowpass filter
    
    Parameters
    ----------
    freq : "int", "float", "astropy.units.Quantity", optional
      the frequency for the lowpass filter, default value is 1 Hz
      
    Return : "mcgpy.timeseries.TimeSeries"
    ------
        (original signal) - (lowpass filtered signal)
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.flattened(1)
    [−691.04563, −728.74299, −612.39823, …, −400.13071, −465.25414, −410.18831]1×10−15T
    '''

    new = flattened(self.value, freq, self.sample_rate).view(type(self))
    self._finalize_attribute(new)
    new._unit = self.unit
    return new

  # fft
  def fft(self):
    '''calculate the fast Fourier transform, FFT
    
    Retrun : "mcgpy.series.FrequencySeries"
    ------
        fft frequency-series
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.fft()
    [92.382265, 16.48454, …,  0.27365534, 0.2273498]1×10−15T
    >>> data.fft().frequencies
    [0, 0.011111352, 0.022222704, …, 511.97778, 511.98889, 512]Hz
    '''
    
    findex, ffty = fft(self, self.sample_rate.value)
    
    new = FrequencySeries(ffty, unit=self.unit, frequencies=findex)
    new.number = self.number
    new.label = self.label
    
    return new
  
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

    Retrun : "mcgpy.series.FrequencySeries"
    ------
        asd frequency-series
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.asd(2,1)
    [16.390747, 62.977136, 149.35229, …, 1.8138222, 1.4555211, 0.93069027]1×10−15THz1/2
    >>> data.asd(2,1).frequencies
    [0, 0.5, 1, …, 511, 511.5, 512]Hz
    '''
    
    nperseg = self._get_value(fftlength)
    overlap = self._get_value(overlap)
    
    findex, asdy = asd(self, self.sample_rate.value, nperseg, overlap, window, average)
    
    asd_unit = 1*self.unit/u.hertz**0.5
    new = FrequencySeries(asdy, unit=asd_unit, frequencies=findex)
    new.number = self.number
    new.label = self.label
  
    return new
  
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

    Retrun : "mcgpy.series.FrequencySeries"
    ------
        psd frequency-series
        
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.psd(2,1)
    [268.6566, 3966.1196, 22306.108, …, 3.2899511, 2.1185417, 0.86618438]1×10−30T2Hz
    >>> data.psd(2,1).frequencies
    [0, 0.5, 1, …, 511, 511.5, 512]Hz
    '''
    
    nperseg = self._get_value(fftlength)
    overlap = self._get_value(overlap)
    
    findex, psdy = psd(self.value, self.sample_rate.value, nperseg, overlap, window, average)
    
    psd_unit = 1*self.unit**2/u.hertz
    new = FrequencySeries(psdy, unit=psd_unit, frequencies=findex)
    new.number = self.number
    new.label = self.label
  
    return new

  # argmax
  def argmax(self):
    '''find the epoch of the maximum value
    
    Return : "astropy.table.Quantity"
    ------
      a timestamp of the maximum value
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.max()
    4480.30971×10−15T
    >>> data.argmax()
    11.3447265625 s
    '''
    return self.times[np.argmax(self.value)]
  
  # argmin
  def argmin(self):
    '''find the epoch of the minimum value
    
    Return : "astropy.table.Quantity"
    ------
      a timestamp of the minimum value
    
    Examples
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.min()
    53.7786021×10−15T
    >>> data.argmin()
    10 s
    '''
    return self.times[np.argmin(self.value)]

  # smooth
  def smooth(self, window_len=20, window='hamming'):
    '''smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    Parameters : "int", "str"
    ----------
      window_len: the dimension of the smoothing window; should be an odd integer
        
      window: the type of window from "flat", "hanning", "hamming", "bartlett", "blackman"
         
              flat window will produce a moving average smoothing.

    Return : "mcgpy.timeseries.TimeSeriesArray"
    -------
      the smoothed signal
        
    
    Example :
    -------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.smooth()
    [0.05400055 0.05393543 0.05380835 ... 0.02055647 0.02056301 0.02056301] 1e-15 T
    
    See also : 
    ---------
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    '''

    # check the paramters
    if window_len<3:
      return self
    
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
      raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
    
    if self.size < window_len:
      raise ValueError("Input vector needs to be bigger than window size.")

    s=np.r_[self[window_len-1:0:-1],self,self[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
      w=np.ones(window_len,'d')
    else:
      w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')

    new = y[window_len//2:1-window_len//2]
    self._finalize_attribute(new)

    return new
        
  
  # slope correction
  def slope_correction(self):
    '''signal slope correction method
       is based on the linear function which obtaines initial and last coorduinates of signal
       
    Return :  "mcgpy.timeseries.TimeSeriesArray"
    ------
      slope adjusted signal or signals
      
    Examples :
    --------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.slope_correction()
    [0.00000000e+00 5.67263211e-04 1.77546869e-03 ... 6.08924282e-05 2.39171516e-07 1.19585758e-07] 1e-15 T
    '''
    a = (self[-1]-self[0])/len(self)
    b = self[0]
    x = np.arange(0, len(self))
    new = self-(a*x+b)
    self._finalize_attribute(new)
    
    return new
      
    
  # peak finder
  def find_peaks(self, height_amp=0.85, threshold=None, distance=None, prominence=None, width=1, wlen=None, rel_height=0.5, plateau_size=None, **kwargs):
    '''Find peaks inside a signal based on peak properties
    
    Parameters : "ini", "float",  "str"
    ------------      
      height_amp : "float", optional
      
          Used for determining maximum height in sample.
      
      threshold : number or ndarray or sequence, optional
        
          Required threshold of peaks, the vertical distance to its neighboring samples. 
          Either a number, None, an array matching x or a 2-element sequence of the former. The first element is always interpreted as the minimal and the second, if supplied, as the maximal required threshold.
      
      distance : number, optional
      
          Required minimal horizontal distance (>= 1) in samples between neighbouring peaks. Smaller peaks are removed first until the condition is fulfilled for all remaining peaks.
      
      prominence : number or ndarray or sequence, optional
      
          Required prominence of peaks. Either a number, None, an array matching x or a 2-element sequence of the former. 
          The first element is always interpreted as the minimal and the second, if supplied, as the maximal required prominence.
      
      width : number or ndarray or sequence, optional
      
          Required width of peaks in samples. Either a number, None, an array matching x or a 2-element sequence of the former. 
          The first element is always interpreted as the minimal and the second, if supplied, as the maximal required width.
      
      wlen : "int", optional
      
          Used for calculation of the peaks prominences, thus it is only used if one of the arguments prominence or width is given. See argument wlen in peak_prominences for a full description of its effects.
      
      rel_height : "float", optional
      
          Used for calculation of the peaks width, thus it is only used if width is given. 
          See argument rel_height in peak_widths for a full description of its effects.
      
      plateau_size : number or ndarray or sequence, optional
      
          Required size of the flat top of peaks in samples. Either a number, None, an array matching x or a 2-element sequence of the former. 
          The first element is always interpreted as the minimal and the second, if supplied as the maximal required plateau size.
    
    
    Return : "mcgpy.timeseries.TimeSeriesArray"
    --------
    
        times of peaks in dataset that satisfy all given conditions
    
    Examples :
    ---------
    >>> from mcgpy.timeseries import TimeSeries
    >>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
    >>> data.find_peaks()
    [1.11948764e+09 1.11948764e+09 1.11948764e+09 1.11948764e+09
     1.11948764e+09 1.11948764e+09 1.11948764e+09 1.11948765e+09
     1.11948765e+09 1.11948765e+09 1.11948765e+09 1.11948765e+09
     1.11948765e+09 1.11948765e+09 1.11948765e+09 1.11948766e+09
     1.11948766e+09 1.11948766e+09 1.11948766e+09 1.11948766e+09
     1.11948766e+09 1.11948766e+09] s
    
    See also:
    "scipy.signal.find_peaks"
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
    
    '''
    
    times = self.times
    height = self.max().value*height_amp

    peaks, _ = find_peaks(self.value, height=height, threshold=threshold, distance=distance, prominence=prominence, width=width, wlen=wlen, rel_height=rel_height, plateau_size=plateau_size)

    return times[peaks]

