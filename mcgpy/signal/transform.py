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

'''transform : signal processing methods: rms, fft, psd, asd, and so on
'''

import numpy as np
from scipy import signal
from astropy.units import Quantity
from warnings import warn

__author__ = 'Phil Jung <pjjung@amcg.kr>'
__all__ = ['rms', 'fft', 'psd', 'asd']

#---- main functions --------------------------------

def rms(series, sample_rate, stride=1, **kwargs):
  '''root mean square, RMS
  
  Parameters
  ----------
  series : "list", "np.ndarray", "astropy.units.Quantity"
      ditital signal
  
  sample_rate : "int", "float"
      sample rate of ditital signal
  
  stride : "int", optional
      stride to calculate RMS,
      default value is 1 second
      
  Raises
  ------
  ValueError
      if the input value is not a numpy array type or a list type
      
  Return : "np.ndarray"
  ------
      the result of RMS 
  '''
  
  _shape_checker(series, rms)
  if isinstance(series, list):
    stride_length = int(sample_rate*stride)
    series_array = np.array(series)
    reshaped = np.reshape(series_array, (len(series)//stride_length, stride_length))
    rms_out = np.empty(0)
    for row in reshaped:
      rms_out = np.append(rms_out, np.sqrt(np.mean(row**2)))
    return rms_out
  
  elif isinstance(series, np.ndarray):
    stride_length = int(sample_rate*stride)
    reshaped = np.reshape(series, (len(series)//stride_length, stride_length))
    rms_out = np.empty(0)
    for row in reshaped:
      rms_out = np.append(rms_out, np.sqrt(np.mean(row**2)))
    return rms_out 
  
  else:
    raise ValueError('given value was no vaild array or list')
  
def fft(series, sample_rate, **kwargs):
  '''fast Fourier transform, FFT
  
  Parameters
  ----------
  series : "list", "np.ndarray", "astropy.units.Quantity"
      ditital signal
  
  sample_rate : "int", "float"
      sample rate of ditital signal

  Return : "tuple"
  ------
  "np.ndarray"
      the result of FFT 
      
  "np.ndarray"
      frequncies of FFT
  '''
  
  _shape_checker(series, fft)
  N = len(series)
  freq_range = np.linspace(0.0, 0.5*sample_rate, N//2)
  fft_vals = np.fft.fft(series)/N
  return freq_range, abs(fft_vals[:N//2])
  
def psd(series, sample_rate, seglength=None, overlap=0, window='hann', average='median', **kwargs):
  '''power spectral density, PSD
  
  Parameters
  ----------
  series : "list", "np.ndarray", "astropy.units.Quantity"
      ditital signal
  
  sample_rate : "int", "float"
      sample rate of ditital signal
      
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

  Return : "tuple"
  ------
  "np.ndarray"
      frequncies of PSD
      
  "np.ndarray"
      the result of PSD 
  '''
  
  _shape_checker(series, psd)
  if seglength is None:
    warn('segmentlength was given to {0}s. it must be less than data length = {1}s, it will be ignored and be set to {1}s'.format(seglength, len(series)/sample_rate))
    nperseg = len(series)
  else:
    nperseg = seglength*sample_rate
  if not overlap != 0:
    overlap = sample_rate*overlap
  
  findex, Pxx_den = signal.welch(series, sample_rate, nperseg=nperseg, noverlap=overlap, window=window, average=average)
  return findex, Pxx_den

def asd(series, sample_rate, seglength=None, overlap=0, window='hann', average='median', **kwargs):
  '''acceleration spectral density, ASD
  
  Parameters
  ----------
  series : "list", "np.ndarray", "astropy.units.Quantity"
      ditital signal
  
  sample_rate : "int", "float"
      sample rate of ditital signal
      
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

  Return : "tuple"
  ------
  "np.ndarray"
      frequncies of ASD
      
  "np.ndarray"
      the result of ASD 
  
  '''
  
  _shape_checker(series, asd)
  findex, Pxx_den = psd(series, sample_rate, seglength, overlap, window, average)
  return findex, Pxx_den**0.5
  
def whiten(series, sample_rate, seglength=None, overlap=0, window='hann', **kwargs):
  '''whitning method will be support
  '''
  None


#---- inherent functions --------------------------------

def _to_value(value):
  try:
    return float(value.value)
  except (AttributeError, TypeError):
    return float(value)
  
def _shape_checker(series, name):
  if np.ndim(series) != 1:
    raise ValueError('Cannot generate {} with {}-dimensional data'.format(name.__name__, np.ndim(series)))
