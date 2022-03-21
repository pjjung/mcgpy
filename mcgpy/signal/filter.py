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

'''filter : time-series filter methods: band-/low-/high-pass and notch filters / flattend filter
'''

import numpy as np
from scipy import signal 

__author__ = 'Phil Jung <pjjung@amcg.kr>'
__all__ = ['bandpass', 'lowpass', 'highpass', 'notch', 'flattend']

#---- main functions --------------------------------

def bandpass(series, lfreq, hfreq, sample_rate, order=4, flattening=True, **kwargs):
  '''bandpass filter
  
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
  
  flattening : Boonlean, potions
      signal flattening option, defaule value is True
  
  Return : "np.ndarray"
  ------
      filted series
  '''
  
  sample_rate, nyq, lfrequency, hfrequency = _to_parameters(sample_rate, lfreq, hfreq)
  a, b = signal.butter(order, [lfrequency/nyq, hfrequency/nyq], btype='band')
  if flattening == False:
    return signal.lfilter(a,b,series)
  elif flattening == True:
    for n in range(2):
      ref = series - series[0]
      series = series - series[0]
      series = signal.lfilter(a,b,series)
      series = (series + ref[0])[::-1]
    return series - np.median(series)

def lowpass(series, freq, sample_rate, order=2, flattening=True, **kwargs):
  '''lowpass filter
  
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
      
  flattening : Boonlean, potions
      signal flattening option, defaule value is True
      
  Return : "np.ndarray"
  ------
      filted series
  '''
  
  sample_rate, nyq, frequency = _to_parameters(sample_rate, freq)
  a, b = signal.butter(order, [frequency/nyq], btype='low')
  
  if flattening == False:
    return signal.lfilter(a,b,series)
  
  elif flattening == True:
    for n in range(2):
      ref = series - series[0]
      series = series - series[0]
      series = signal.lfilter(a,b,series)
      series = (series + ref[0])[::-1]
    return series - np.median(series)

def highpass(series, freq, sample_rate, order=2, flattening=True, **kwargs):
  '''highpass filter
  
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
  
  flattening : Boonlean, potions
      signal flattening option, defaule value is True
  
  Return : "np.ndarray"
  ------
      filted series
  '''
  
  sample_rate, nyq, frequency = _to_parameters(sample_rate, freq)
  a, b = signal.butter(order, [frequency/nyq], btype='high')
  if flattening == False:
    return signal.lfilter(a,b,series)          
  elif flattening == True:
    for n in range(2):
      ref = series - series[0]
      series = series - series[0]
      series = signal.lfilter(a,b,series)
      series = (series + ref[0])[::-1]
    return series - np.median(series)
  
def notch(series, freq, sample_rate, Q=30, flattening=True, **kwargs):
  '''notch or bandstop filter

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
  
  flattening : Boonlean, potions
      signal flattening option, defaule value is True
  
  Return : "np.ndarray"
  ------
      filted series
  '''
  
  sample_rate, nyq, frequency = _to_parameters(sample_rate, freq)
  a, b = signal.iirnotch(frequency, Q, sample_rate)
  if flattening == False:
    return signal.lfilter(a,b,series)
  elif flattening == True:
    for n in range(2):
      ref = series - series[0]
      series = series - series[0]
      series = signal.lfilter(a,b,series)
      series = (series + ref[0])[::-1]
    return series - np.median(series)

def flattend(series, freq, sample_rate, order=2, **kwargs):
  '''flatten a wave form by a lowpass filter

  Parameters
  ----------
  series : "list", "np.ndarray", "astropy.units.Quantity"
    ditital signal

  freq : "int", "float", "astropy.units.Quantity"
    the frequency for the lowpass filter

  sample_rate : "int", "float", "astropy.units.Quantity"
    sample rate of ditital signal

  Return : "mcgpy.timeseries.TimeSeries"
  ------
      (original series) - (lowpass filtered series)
  '''
  
  sample_rate, nyq, frequency = _to_parameters(sample_rate, freq)
  a, b = signal.butter(order, [frequency/nyq], btype='low')
  for n in range(2):
    ref = signal.lfilter(a,b,series)
    series = (series - ref)[::-1]
  return series - np.median(series)
  
  
#---- inherent functions --------------------------------

def _to_value(value):
  try:
    return float(value.value)
  except (AttributeError, TypeError):
    return float(value)

def _to_parameters(sample_rate, *args):
  sample_rate = _to_value(sample_rate)
  
  if len(args) == 1:
    frequency = _to_value(args[0])
    
    return sample_rate, 0.5*sample_rate, frequency
  
  elif len(args) == 2:
    lfrequency = _to_value(min(args))
    hfrequency = _to_value(max(args))
    
    return sample_rate, 0.5*sample_rate, lfrequency, hfrequency
  
  else:
    raise ValueError('Too many arguments were inputted')
