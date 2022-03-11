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

'''_fkd : the class to read an KDF file and convert it to "mcgpy.Array" 
'''

import sys
import os 
import numpy as np

from ..time import tconvert
from ..channel import ChannelActive
from ._array import Array

__author__ = 'Phil Jung <pjjung@amcg.kr>'

#---- main class --------------------------------
class KDF:
  def __init__(self, path, *args ,**kwargs):
    '''initialize arguments and check the reliability
    
    Parameters
    ----------
    path : "str"
        the direction of a KDF file
    
    Raises
    ------
    IOError
        if the given file direction did not exist or did not a KDF format
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
    
    _index = self._parameter_checker(number, label) 
    timeseries, metadata = self._get_data(_index)
    
    return Array(timeseries, metadata)
  
  ##---- Inherent properties -------------------------------- 
  def _io_checker(self, path):
    extension = path.split('.')[-1]
    if os.path.isfile(path) and extension != 'kdf':
      raise IOError('illegal file format was inserted')
      
  def _parameter_checker(self, number, label):
    if number is not None and label is None:
      active_channel_numbers = ChannelActive(self.path).get_number()
      if int(number) in active_channel_numbers:
        return active_channel_numbers.index(int(number))
      else:
        raise ValueError('{}-number channel did not exist in given KDF file')
    elif number is None and label is not None:
      active_channel_labels = ChannelActive(self.path).get_label()
      if label in active_channel_labels:
        return active_channel_labels.index(label)
      else:
        raise ValueError('{} channel did not exist in given KDF file')
    elif number is not None and label is not None:
      raise TypeError('read method task 1 positional argument but 2 ware given')
    else:
      raise TypeError('read method missing 1 required positional argument: "number" or "label"')
      
  def _get_data(self, index):
    ## read header of KDF
    data_size = os.path.getsize(self.path)
    with open(self.path, 'br') as f:
      code = f.read(1)
      biosemi = f.read(7).decode('ascii').strip()
      
      subject_info = f.read(80).decode('ascii').strip()
      recording_info = f.read(80).decode('ascii').strip()
      
      try:
        system_gain = int(recording_info.split(' ')[4])
      except IndexError:
        system_gain = 3
        
      date_info = f.read(8).decode('ascii').strip() #DD.MM.YY
      time_info = f.read(8).decode('ascii').strip() #hh.mm.ss
      datetime_info = self._convert_datetime(date_info, time_info)
      timestamp = tconvert(datetime_info)
      
      header_byte = int(f.read(8).decode('ascii').strip())
      data_format = f.read(44).decode('ascii').strip()  #24 bit
      
      data_records = int(f.read(8).decode('ascii').strip())   #[seconds], -1 means unkonwn
      duration = int(f.read(8).decode('ascii').strip())
      
      channels_number = int(f.read(4).decode('ascii').strip())
      channel_labels = f.read(16*channels_number).decode('ascii')

      coil_types = f.read(40*channels_number).decode('ascii')

      units = f.read(8*(channels_number)).decode('ascii')

      minimum_range = f.read(8*(channels_number)).decode('ascii')
      minimum_range = np.array([float(minimum_range[i*8:(i+1)*8].strip()) for i in range(channels_number-1)])

      maximum_range = f.read(8*(channels_number)).decode('ascii')
      maximum_range = np.array([float(maximum_range[i*8:(i+1)*8].strip()) for i in range(channels_number-1)])

      digital_minimum = f.read(8*(channels_number)).decode('ascii')
      digital_minimum = np.array([float(digital_minimum[i*8:(i+1)*8].strip()) for i in range(channels_number-1)])

      digital_maxmum = f.read(8*(channels_number)).decode('ascii')
      digital_maxmum = np.array([float(digital_maxmum[i*8:(i+1)*8].strip()) for i in range(channels_number-1)])

      prefiltering = f.read(80).decode('ascii').strip()
      sample_rate = int(f.read(8).decode('ascii'))
      recording_time =  int((data_size - header_byte) / (channels_number * sample_rate * 3)) #mesearment time have to be equal to data_records time

      gain = self._gain(system_gain, minimum_range, maximum_range)
      count = 3*sample_rate

      bdata = np.fromfile(f, offset=0, dtype=np.uint8)
      datasets = bdata.reshape(int(bdata.shape[0]/count), count)
      f.close()
      
      metadata = {'biosemi':biosemi, 'info':subject_info, 
                  'datetime':datetime_info, 't0':timestamp, 'duration':recording_time, 
                  'number':int(ChannelActive(self.path).get_number()[index]), 'label':str(ChannelActive(self.path).get_label()[index]),
                  'sample_rate':sample_rate}
      
      return self._make_timeseries(index, datasets, sample_rate, recording_time, gain), metadata
  
  def _convert_datetime(self, date_info, time_info):
    for i, value in enumerate(date_info.split('.')[::-1]):
      if i == 0:
        YY = int('20'+value)
      elif i == 1:
        MM = int(value)
      elif i == 2:
        DD = int(value)
    for j, value in enumerate(time_info.split('.')):
      if j == 0:
        hh = int(value)
      elif j == 1:
        mm = int(value)
      elif j == 2:
        ss = int(value)
    return '{}-{}-{} {}:{}:{}'.format(YY,MM,DD,hh,mm,ss)  
    
  def _make_timeseries(self, index, datasets, sampling_rate, recording_time, gain):
    ch_timeseries = np.empty(0)
    for second, dataset in enumerate(np.array_split(datasets, recording_time)):
      ch_data = np.delete(dataset, -1, axis=0)[index]
      if second <= recording_time:
        data = ch_data.reshape(sampling_rate, 3)
        tmp_bin = list()
        for row in data:
          tmp_bin.append(self._bytebuffer(row))
        rcpn = np.array(self._remove_circuit_pulse_noise(tmp_bin)).astype(np.int32)
        decimated_signal = self._signal_decimate(rcpn, sampling_rate, decimating_factor=1)
        
        ch_timeseries = np.append(ch_timeseries, decimated_signal)
      else:
        break
        
    if gain.size != 0:
      gain_value = np.divide(gain, 838860.8)[index]
      return np.multiply(ch_timeseries, gain_value)
    else:
      return ch_timeseries
    
  def _remove_circuit_pulse_noise(self, data):
    length = len(data)
    data.append(np.median(data).astype(np.int32))
    for i in range(length+1):
      abs_data = np.abs(data)
      max_value = abs_data.max()
      max_index = int(np.where(abs_data == max_value)[0][0])
      threshold = abs_data[max_index+1]*100
      if max_value > threshold:
        data[max_index] = data[max_index+1]
        continue
      else:
        break
    del data[-1]
    
    return data
    
  def _gain(self, system_gain, minimum_range, maximum_range):
    if system_gain != 2 or system_gain != 3: #default
      gain = np.multiply((maximum_range - minimum_range),0.5*1000).astype(np.float32)
    elif system_gain == 2:
      gain_list = [1.140000000000,
                  1.064689748547,
                  1.070348223079,
                  1.050158169168,
                  1.060617048626,
                  1.059086250139,
                  1.126160308754,
                  1.077326284194,
                  1.062401477637,
                  1.152351232444,
                  1.065760732372,
                  1.075829971346,
                  1.055526677748,
                  1.064517859654,
                  1.166788764423,
                  1.079126627173,
                  1.080095985567,
                  1.062509901709,
                  1.065555690346,
                  1.078407694924,
                  1.150345577639,
                  1.077350401531,
                  1.192532578579,
                  1.061794750449,
                  1.061089271223,
                  1.085328405243,
                  1.052599945100,
                  1.428122894033,
                  1.091450871449,
                  1.061175768896,
                  1.410562003331,
                  1.433198172062,
                  1.140000000000,
                  1.301986732547,
                  1.415893602342,
                  1.191230725471,
                  1.059633080335,
                  1.086617814525,
                  1.063616086146,
                  1.138060094660,
                  1.047281700359,
                  1.076386919286,
                  1.151940116141,
                  1.058986024518,
                  1.077617448931,
                  1.140000000000,
                  1.030989030763,
                  1.073524410944,
                  1.090633751181,
                  1.054948264372,
                  1.138199158978,
                  1.071383292277,
                  1.040416960920,
                  1.137045026111,
                  1.048734102818,
                  1.149064905471,
                  1.028813063165,
                  1.078903604167,
                  1.140000000000,
                  1.199994033713,
                  1.079938886773,
                  1.033233807718,
                  1.044074911433,
                  1.072169537215,
                  1.176435594141,
                  1.037858286672,
                  1.148428378168,
                  1.174842066022,
                  1.020914518073,
                  1.038982376505,
                  1.173348158927,
                  1.044333416997,
                  1.173844076390,
                  1.042117099332,
                  1.055573343415,
                  1.030751837315,
                  1.039936752130,
                  1.025335616008,
                  1.060059307272,
                  1.055810015441,
                  1.036717322305,
                  1.024154426560,
                  1.143227568004,
                  1.140000000000,
                  1.072616190496,
                  1.150946714058,
                  1.051182229301,
                  1.049941092044,
                  1.182420127874,
                  1.045531484438,
                  1.026363065545,
                  1.041587132894,
                  1.053819344405,
                  1.071080545675,
                  1.063351898675,
                  1.057459720025,
                  1.064779710382,
                  1.075071719141,
                  1.038966960226,
                  1.044794054628,
                  1.098482332885,
                  1.061290241370,
                  1.066669825734,
                  1.029183020706,
                  1.055185392919,
                  1.054790187550,
                  1.060563509756,
                  1.053508675057,
                  1.054081998637,
                  1.061709397420,
                  1.046475944581,
                  1.026947892671,
                  1.084362963570,
                  1.058068114132,
                  1.055476313546,
                  1.433779965563,
                  1.103192692009,
                  1.418022365520,
                  1.140000000000,
                  1.140000000000,
                  1.120565662306,
                  1.029084691992,
                  1.361926919837,
                  1.039724141294,
                  1.083415637174,
                  1.024977588840,
                  1.076791999544,
                  1.067673594861,
                  1.057560953367,
                  1.025654043117,
                  1.063429059235,
                  1.049615198078,
                  1.168312578411,
                  1.058229875971,
                  1.055080985371,
                  1.058835173974,
                  1.031553853911,
                  1.076070448322,
                  1.046594225134,
                  1.049261554357,
                  1.124285111176,
                  1.183791924336,
                  1.068252949333,
                  1.051679022988,
                  1.037103549443,
                  1.069314059916,
                  1.050266035040,
                  1.044657590135,
                  1.056374100329,
                  1.069658646060,
                  1.027078560117,
                  1.060769935730,
                  1.140000000000,
                  1.140000000000,
                  1.140000000000,
                  1.140000000000,
                  1.140000000000,
                  1.140000000000,
                  1.140000000000,
                  1.140000000000]
      for i in range(channels_number-1):
        if i == 0:
          gain = np.array(gain_list[i]*1000000, dtype=np.float32)
        else:
          gain = np.append(gain, gain_list[i]*1000000)

    elif system_gain == 3:
      gain_list = [1.314415646676,
                  -1.139521315572,
                  -1.161156095399,
                  -1.138594234812,
                  -1.152910591016,
                  -1.144180498722,
                  -1.167850684976,
                  -1.174256750587,
                  -1.171135209544,
                  -1.188198472199,
                  -1.159384966735,
                  -1.186816634865,
                  -1.189088031125,
                  -1.160415778838,
                  -1.167612881852,
                  -1.172338258359,
                  -1.142680802565,
                  -1.161401278128,
                  -1.140634914326,
                  -1.167334552228,
                  -1.149613253317,
                  -1.163753091030,
                  -1.176427010234,
                  -1.196641095214,
                  -1.175096984100,
                  -1.171878190721,
                  -1.198702243888,
                  -1.199416378432,
                  -1.190142329984,
                  -1.179703459870,
                  -1.192893734116,
                  -1.178096925690,
                  -1.142894494732,
                  -1.144662220955,
                  -1.101100017652,
                  -1.164585814441,
                  -1.134294711830,
                  -1.150047404218,
                  -1.200757756690,
                  -1.150956803556,
                  -1.152092961320,
                  -1.211468966197,
                  -1.162318388020,
                  -1.166083266478,
                  -1.169919135388,
                  -1.184487574481,
                  -1.179890735752,
                  -1.241244380666,
                  -1.128299245860,
                  -1.128866308748,
                  -1.125745453379,
                  -1.140238704396,
                  -1.145380829858,
                  -1.147378606864,
                  -1.141008180818,
                  -1.159056513792,
                  -1.151982636796,
                  -1.152855479899,
                  -1.185094411175,
                  -1.159483089406,
                  -1.162791536264,
                  -1.178744039646,
                  -1.165747629920,
                  -1.177771666268,
                  -1.182690586699,
                  -1.253801830758,
                  -1.200224434090,
                  -1.182591964472,
                  -1.190679374430,
                  -1.171493736460,
                  -1.189300076280,
                  -1.178677452144,
                  -1.199821372178,
                  -1.180688492857,
                  -1.172903561695,
                  -1.193767676052,
                  -1.187936200647,
                  -1.194971602916,
                  -1.200665692316,
                  -1.187762287541,
                  -1.160559041705,
                  -1.183803636741,
                  -1.183725349092,
                  -1.160610736566,
                  -1.198013738260,
                  -1.174036103724,
                  -1.200396954508,
                  -1.184666792439,
                  -1.192628070102,
                  -1.183863360496,
                  -1.196667288150,
                  -1.195469674868,
                  -1.184413988755,
                  -1.168998371815,
                  -1.168344247902,
                  -1.185641255590,
                  -1.152116944560,
                  -1.153106434254,
                  -1.115210106628,
                  -1.140000000000,
                  -1.141510394002,
                  -1.148356517140,
                  -1.164290291130,
                  -1.150998795176,
                  -1.170569642247,
                  -1.154314753753,
                  -1.176852873165,
                  -1.164542559894,
                  -1.188805375040,
                  -1.168318269320,
                  -1.180019786326,
                  -1.180052827406,
                  -1.143834248944,
                  -1.148601659913,
                  -1.140185607063,
                  -1.130807828720,
                  -1.147620518252,
                  -1.170586905844,
                  -1.159476934454,
                  -1.136407701395,
                  -1.184261553467,
                  -1.277222064545,
                  -1.181568750923,
                  -1.175547856815,
                  -1.200360353130,
                  -1.162449954141,
                  -1.157571050937,
                  -1.179993190698,
                  -1.221861343715,
                  -1.219744756909,
                  -1.140000000000,
                  -1.190960674359,
                  -1.231009980378,
                  -1.197872049925,
                  -1.183071121343,
                  -1.190111901862,
                  -1.209167666825,
                  -1.199752521400,
                  -1.207436252164,
                  -1.200229494167,
                  -1.184392949574,
                  -1.186650897704,
                  -1.181283374572,
                  -1.201409467875,
                  -1.145220336358,
                  -1.158486344606,
                  -1.149954651365,
                  -1.185454776512,
                  -1.185452100080,
                  -1.174776892114,
                  -1.184630266220,
                  -1.210898000851,
                  -1.140000000000,
                  -1.140000000000,
                  -1.140000000000,
                  -1.140000000000,
                  -1.140000000000,
                  -1.140000000000,
                  -1.140000000000,
                  -1.140000000000]
      for i in range(channels_number-1):
        if i == 0:
          gain = np.array(gain_list[i]*1000000, dtype=np.float32)
        else:
          gain = np.append(gain, gain_list[i]*1000000)
    return gain
    
  def _bytebuffer(self, segment):
    x = segment[0]
    y = segment[1]
    z = segment[2]

    u16 = np.frombuffer(x.tobytes() + y.tobytes(), dtype=np.uint16)[0]
    u32 = np.frombuffer(u16.tobytes() + np.uint16(z).tobytes(), dtype=np.uint32)[0]
    i32 = np.int32(u32)

    if i32 > 8388607:
      i32 = i32 - 16777216

    return i32

  def _signal_decimate(self, signal, sampling_rate, decimating_factor):
    return signal.reshape(sampling_rate//decimating_factor, decimating_factor)[:,0]
