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

'''_fkd2hdf : the class to convert an KDF format to an HDF5 format  
'''

import h5py
import numpy as np

from ._kdf import KDF
from ..channel import (ChannelConfig, ChannelActive)

__author__ = 'Phil Jung <pjjung@amcg.kr>'

#---- main functions --------------------------------
class KDF2HDF:
  def __init__(self, kdf, config, *args, **kwargs):
    '''initialize arguments and check the reliability
    
    Parameters
    ----------
    kdf : "str"
        the direction of a KDF file
    
    config : "str"
        the direction of a configuration file which contains channel's directions, positions, numbers, and labels
    
    Raises
    ------
    IOError
        if the given file direction did not exist or did not a KDF format
    '''
    
    self.kdf = kdf
    self.config = config

  def write(self, path=None, *args, **kwargs):
    '''convert an KDF format to an HDF5 format and write it in the input folder directory
    
    Parameters
    ----------
    path : "str"
        the folder direction user wnat to write it
        if input is None, a converted file saves in the same folder
        
    Note
    ----
    Hierarchical structure of HDF5 file will be
    GROUP : number_label
        DATA : single-channel time-series
            METADATA : biosemi, info, datetime, t0, duration, number, label, sample_rate
        POSITION : position information of the channel
        DIRECTION : direction information of the channel
        
    example
    | 01_X1
        |- timeseries
          [1,2,3,4,5...]
            |- {"biosemi":"HOSPITAL", "duration":90, ...}
        |- position
          [0,0,0]
        |- direction
          [1,0,0]
    .
    .
    .
    '''
    
    if path is None:
      path = '/'.join(kdf_path.split('/')[:-1])
    else:
      path = self._path_syntax(path)
    
    data = KDF(self.kdf)
    
    active_channels = ChannelActive(self.kdf).get_table()
    positions = ChannelConfig(self.config).get('positions')
    directions = ChannelConfig(self.config).get('directions')
 
    hdf5_path = path + '/' + self.kdf.split('/')[-1].replace('kdf', 'hdf5')
    with h5py.File(hdf5_path, 'w') as f:
      for row in active_channels:
        number, label = int(row['number']), str(row['label']), 
        index = number-1

        if number < 10:
          group = f.create_group('0{}_{}'.format(number, label))
        else:
          group = f.create_group('{}_{}'.format(number, label))
        ch_data = data.read(label=label)
        dataset1 = group.create_dataset('timeseries', data=ch_data)
        dataset2 = group.create_dataset('position', data=positions[index]['positions'])
        dataset3 = group.create_dataset('direction', data=directions[index]['directions'])
        
        metadata = {'biosemi':str(ch_data.biosemi), 'info':str(ch_data.info), 
                    'datetime':ch_data.datetime, 't0':ch_data.t0, 'duration':ch_data.duration, 
                    'number':number, 'label':label,
                    'sample_rate':ch_data.sample_rate}
        dataset1.attrs.update(metadata)
        
      f.close()
    
  #---- inherent functions --------------------------------
  def _path_syntax(self, path):
    if path.split('/')[-1] == '':
      path = path[:-1]
    return path
