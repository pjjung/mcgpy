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

'''fieldmap : a class to get magnetic field map and arrow map
'''

import numpy as np
from astropy.units import (second, Quantity, Unit)
from astropy.table import QTable
from warnings import warn

from ..time import tconvert
from ..timeseries import TimeSeriesArray
from .leadfield import LeadField

__author__ = 'Phil Jung <pjjung@amcg.kr>'

class FieldMap(Quantity):
  def __new__(cls, data,
              sourcegrid_width=240, sourcegrid_height=-40, sourcegrid_interval=16,
              sensorgrid_width=400, sensorgrid_height=40, sensorgrid_interval=25,
              baseline=50, axis='z', conduct_model='horizontal', eigenvalues=10, **kwargs):
    '''calculate magnetic field maps on the sersor plane
    
    Parameters
    ----------
    data : "mcgpy.timeseriesarra.TimeSeriesArray"
        MCG dataset 1) at the certain time point
                    2) between certain duration
    
    sourcegrid_width : "int", "float", "astropy.units.Quantity", optional
        width of source grid, default value is 240 [mm]
    
    sourcegrid_height : "int", "float", "astropy.units.Quantity", optional
        height of source grid, default value os -40 [mm]
    
    sourcegrid_interval : "int", "float", "astropy.units.Quantity", optional
        interval of cells on source grid, default value is 16 [mm]
    
    sensorgrid_width : "int", "float", "astropy.units.Quantity", optional
        width of sensor grid, default value is 400 [mm]
    
    sensorgrid_height : "int", "float", "astropy.units.Quantity", optional
        height of sensor grid, defualt value is 40 [mm]
    
    sensorgrid_interval : "int", "float", "astropy.units.Quantity", optional
        interval of cells on sensor grid, default value is 25 [mm]
    
    baseline : "int", "float", "astropy.units.Quantity", optional
        length of baseline (Z-axis length of sensor), defualt value is 50 [mm]
    
    axis : "str", optional
        axis of magnetic vectors on sensor grid
    
    conduct_model : "str", optional
        conduct model about sources
    
    eigenvalues : "int", optional
        the number of eigenvalues to get quasi-inverser lead field matrix
        
    Raises
    ------
    TypeError
        if input data type is not "mcgpy.timeseriesarray.TimeSeriesArray"
        
    Return : "mcgpy.numerical.FieldMap"
    ------
    if the dimension of input dataset is one
        2D-array, amplitude of given direction of magnetic vector on sensor plane
        
    if the dimension of input dataset is two
        3D-array, amplitude of given direction of magnetic vectors on sensor plane
        
        
    Examples
    --------
    >>> from mcgpy.timeseriesarray import TimeSeriesArray
    >>> from mcgpy.numeric import LeadField
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> epoch_dataset = dataset.at(1126259462)
    >>> LeadField(epoch_dataset)
    [[−1.2890067, −1.4466162, −1.6401107, …, 0.17438883, 0.30280878, 0.38030763], [−1.4262029, −1.6297339, −1.9009002, …, 0.4317918, 0.53622291, 0.58182473], 
    [−1.5804608, −1.8479563, −2.234106, …, 0.84135491, 0.86858131, 0.84406456], …, [−0.76191537, −0.75202421, −0.66326362, …, 2.2549908, 1.8901924, 1.6201124]]1×10−15T
    >>>
    >>> duration_dataset =  dataset.crop(1126259462, 1126259470)
    >>> LeadField(epoch_dataset)
    [[[−1.2890067, −1.4466162, −1.6401107, …, 0.17438883, 0.30280878, 0.38030763], ..., [−1.4262029, −1.6297339, −1.9009002, …, 0.4317918, 0.53622291, 0.58182473]], 
    ...
    [[−1.5804608, −1.8479563, −2.234106, …, 0.84135491, 0.86858131, 0.84406456], ..., [−0.76191537, −0.75202421, −0.66326362, …, 2.2549908, 1.8901924, 1.6201124]]]1×10−15T
    '''

    cls._axis = axis
    cls._conduct_model = conduct_model
    cls._eigenvalues = eigenvalues
    
    if np.ndim(data) == 1 and isinstance(data, TimeSeriesArray):
      cls._ndim = 1
      positions = data.positions
      directions = data.directions
      unit = data.unit
      
      _leadfield = LeadField(positions, directions, 
                            sourcegrid_width, sourcegrid_height, sourcegrid_interval, 
                            baseline, axis, conduct_model)
      
      X, Y, Z = _leadfield.field_map(data, sensorgrid_width, sensorgrid_height, sensorgrid_interval, eigenvalues)
      
      cls._X = Quantity(X, Unit('mm')) 
      cls._Y = Quantity(Y, Unit('mm'))
      new = Quantity(Z, unit).view(cls)
       
      for key in ['t0', 'datetime']:
        _key = '_{}'.format(key)
        try:
          value = getattr(data, key)
          setattr(new, _key, value)
        except AttributeError:
          pass
      
      return new
      
    elif np.ndim(data) == 2 and isinstance(data, TimeSeriesArray):
      cls._ndim = 2
      if data.duration.value > 0.1:
        warn('RuntimeWarning: {} dataset was given to {}'.format(data.duration, cls.__name__))
      positions = data.positions
      directions = data.directions
      unit = data.unit
      
      for i, epoch_data in enumerate(data.T):
        if i == 0:
          _leadfields = LeadField(positions, directions, 
                                  sourcegrid_width, sourcegrid_height, sourcegrid_interval, 
                                  baseline, axis, conduct_model)
          
          cls._X, cls._Y, Zs = _leadfields.field_map(epoch_data, sensorgrid_width, sensorgrid_height, sensorgrid_interval, eigenvalues)
          
          leadfield_shape = _leadfields.shape
          Zs_shape = Zs.shape
          
        else:
          _leadfield = LeadField(positions, directions, 
                                 sourcegrid_width, sourcegrid_height, sourcegrid_interval, 
                                 baseline, axis, conduct_model)
          X, Y, Z = _leadfield.field_map(epoch_data, sensorgrid_width, sensorgrid_height, sensorgrid_interval, eigenvalues)
          
          Zs = np.vstack((Zs, Z))
      
      cls._X = Quantity(X, Unit('mm'))
      cls._Y = Quantity(Y, Unit('mm'))
      new = Quantity(Zs.reshape(i+1, Zs_shape[0], Zs_shape[1]), unit).view(cls)
      
      for key in ['sample_rate', 't0', 'datetime', 'times', 'dt', 'duration']:
        _key = '_{}'.format(key)
        try:
          value = getattr(data, key)
          setattr(new, _key, value)
        except AttributeError:
          pass
      
      return new
      
    else:
      raise TypeError('illegal data type was given to {}, it takes TimeSeriesArray only'.format(cls.__name__))
      
      
  ##---- Inherent functions -------------------------------- 
  def _get_arrows_table(self, data, meta):
    # calculate arrow vector
    arrow_vectors = np.gradient(data, axis=0) - 1j*np.gradient(data, axis=1)
    # organize X and Y coordinates
    xs, ys = self.X.flatten().value, self.Y.flatten().value
    
    # set empty lists for making table
    tails, arrows, heads, distances, angle = list(), list(), list(), list(), list()
    
    # organize table contents
    for x, y, vector in zip(xs, ys, arrow_vectors.flatten().value): 
      head_x, head_y = x+np.real(vector), y+np.imag(vector)
      Euclidean_distance = abs(vector)*Unit('amp meter')*10**-9
      current_angle = -180*(np.angle(vector)/np.pi)*Unit('degree')
      
      tails.append((x, y))
      arrows.append(vector)
      heads.append((head_x, head_y))
      distances.append(Euclidean_distance)
      angle.append(current_angle)
    
    return QTable([tails, heads, arrows, distances, angle],
                  names=('tail', 'head', 'vector', 'distance', 'angle'),
                  meta=meta)

  def _get_pole_information(self, data):
    # data flattening
    flattend_data = data.flatten()
    # organize X and Y coordinates
    xs, ys = self.X.flatten().value, self.Y.flatten().value
    
    # find maximum and minimum values
    max_value = flattend_data.max()
    min_value = flattend_data.min()
    max_index = np.argmax(flattend_data)
    min_index = np.argmin(flattend_data)
    
    # calculate Max/Min ratio
    ratio = abs(max_value/min_value)
    
    # calculate pole distance and angle
    vector = (xs[max_index] - xs[min_index]) + 1J*(ys[max_index] - ys[min_index])
    distance = abs(vector)*Unit('mm')
    angle = -180*(np.angle(vector)/np.pi)*Unit('degree')
    
    # make table contents and return it
    return [(xs[min_index], ys[min_index]), (xs[max_index], ys[max_index]), vector, distance, angle, ratio]
  
    
  ##---- Properties --------------------------------
  # X
  @property
  def X(self):
    try:
      return self._X
    except AttributeError:
      pass
  
  # Y
  @property
  def Y(self):
    try:
      return self._Y
    except AttributeError:
      pass
  
  # sample rate
  @property
  def sample_rate(self):
    try:
      return self._sample_rate
    except AttributeError:
      pass
  
  # t0
  @property
  def t0(self):
    try:
      return self._t0
    except AttributeError:
      pass
  
  # datetime
  @property
  def datetime(self):
    try:
      return self._datetime
    except AttributeError:
      pass
  
  # times
  @property
  def times(self):
    try:
      return self._times
    except AttributeError:
      pass
  
  # dt
  @property
  def dt(self):
    try:
      return self._dt
    except AttributeError:
      pass
  
  # duration
  @property
  def duration(self):
    try:
      return self._duration
    except AttributeError:
      pass
  
  ##---- Methods --------------------------------
  def currents(self):
    '''get tangential field map
    
    Return
    ------
    if the dimension of input dataset is one : "mcgpy.numerical.FieldMap"
        2D-array, amplitude of current magnitudes on sensor plane
        
    if the dimension of input dataset is two : "mcgpy.numerical.FieldMap"
        3D-array, amplitude of current magnitudes on sensor plane 
    
    Examples
    --------
    >>> from mcgpy.timeseriesarray import TimeSeriesArray
    >>> from mcgpy.numeric import LeadField
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> epoch_dataset = dataset.at(1126259462)
    >>> LeadField(epoch_dataset).currents()
    [[5.80895955e-08 6.82033252e-08 8.38246186e-08 ...
      1.15054266e-07 1.04146993e-07 9.39165794e-08]
     [7.09999483e-08 8.75171891e-08 1.14528064e-07 ...
      1.44635222e-07 1.21560702e-07 1.04386546e-07]
     [1.00648263e-07 1.33912668e-07 1.90724137e-07 ...
      1.92781156e-07 1.53434507e-07 1.24748848e-07]
     ...
     [1.03979718e-07 1.27879891e-07 1.61285186e-07 ...
      1.89137749e-07 1.54725988e-07 1.27253331e-07]
     [8.71076169e-08 9.96315932e-08 1.19166692e-07 ...
      1.35433846e-07 1.16556350e-07 9.96535657e-08]
     [7.68162949e-08 8.32770941e-08 9.37287466e-08 ...
      1.11205662e-07 9.82416776e-08 8.55364650e-08]] A m
    '''
    
    if self._ndim == 1:
      return np.sqrt(np.gradient(self.value, axis=0)**2 + np.gradient(self.value, axis=1)**2)*Unit('amp meter')*10**-9
    
    elif self._ndim == 2:
      for i, epoch_date in enumerate(self.value):
        if i == 0:
          tangentials = np.sqrt(np.gradient(epoch_date, axis=0)**2 + np.gradient(epoch_date, axis=1)**2)*Unit('amp meter')*10**-9
        else:
          tangentials = np.vstack((tangentials, 
                                  np.sqrt(np.gradient(epoch_date, axis=0)**2 + np.gradient(epoch_date, axis=1)**2)*Unit('amp meter')*10**-9))
          
        return tangentials
  
  def arrows(self):
    '''calculate current vectors on the sensor plane and make table
    
    Return
    ------
    if the dimension of input dataset is one : "astropy.table.QTable"
        table contains current arrows on sensor plane: tail coordinate, head coordinate, vector, and distance
        
    if the dimension of input dataset is two : "dict", "astropy.table.QTable"
        dictionanty consists of a table at each time
    
    Examples
    --------
    >>> from mcgpy.timeseriesarray import TimeSeriesArray
    >>> from mcgpy.numeric import LeadField
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> epoch_dataset = dataset.at(1126259462)
    >>> LeadField(epoch_dataset).arrows()
    tail 	              head	                 vector	    distance
    float64	              float64	             complex128	    float64
    (-200.0,0.0,-200.0)	  (-200.13,0.0,-200.15)	(-0.13-0.15j) 	0.20
    (-175.0,0.0,-200.0)	  (-175.18,0.0,-200.17)	(-0.18-0.17j)  	0.25
    .
    .
    .
    >>> duration_dataset =  dataset.crop(1126259462, 1126259470)
    >>> LeadField(epoch_dataset)
    {1126259462:
    tail 	              head	                 vector	    distance
    float64	              float64	             complex128	    float64
    (-200.0,0.0,-200.0)	  (-200.13,0.0,-200.15)	(-0.13-0.15j) 	0.20
    (-175.0,0.0,-200.0)	  (-175.18,0.0,-200.17)	(-0.18-0.17j)  	0.25
    .
    .
    .
    ,...}
    '''
    
    # get tables of arrow information
    if self._ndim == 1:
      meta = {'unit':Unit('mm'), 't0':self.t0, 'datetime':self.datetime, 'field direction':self._axis, 'conduct model':self._conduct_model, 'eigenvalues':self._eigenvalues}
      return self._get_arrows_table(self, meta)

    elif self._ndim == 2:
      _t0 = self.t0
      tables = dict()
      for n, epoch_data in enumerate(self):
        epoch = _t0 + (n*self.sample_rate.value)*second
        epoch_datetime = tconvert(epoch.value)
        meta = {'unit':Unit('mm'), 't0':epoch, 'datetime':epoch_datetime, 'field direction':self._axis, 'conduct model':self._conduct_model, 'eigenvalues':self._eigenvalues}
        tables[epoch] = self._get_arrows_table(epoch_data, meta)
      
      return tables     
  
  def pole(self):
    '''calculate a field current vector on the sensor plane and make table
    
    Return
    ------
    if the dimension of input dataset is one : "astropy.table.QTable"
        tabel contains a field current arrow on sensor plane: minimum coordinates, maximum coordinate, vector, distance, anngle, and ratio
        
    if the dimension of input dataset is two : "astropy.table.QTable"
        tabel contains a field current arrows on sensor plane during at each time: minimum coordinates, maximum coordinate, vector, distance, anngle, and ratio
    
    Examples
    --------
    >>> from mcgpy.timeseriesarray import TimeSeriesArray
    >>> from mcgpy.numeric import LeadField
    >>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
    >>> epoch_dataset = dataset.at(1126259462)
    >>> LeadField(epoch_dataset).pole()
    type         	1126259462 s
    str14        	object
    min coordinate	(-75.0, -100.0)
    max coordinate	(75.0, 100.0)
    vector	        (150+0j)
    distance	    150.0
    angle	        -0.0 deg
    ratio	        0.76948964274897
    >>>
    >>> duration_dataset =  dataset.crop(1126259462, 1126259470)
    >>> LeadField(epoch_dataset)
    type         	1126259462 s         	1126259462.29296875 s         	...
    str14        	object         	        object                      	...
    min coordinate	(-75.0, -100.0)         (-75.0, -100.0)             	...
    max coordinate	(75.0, 100.0)           (75.0, 100.0)               	...
    vector	        (150+0j)                (150+0j)         	            ...
    distance	    150.0                   150.0         	                ...
    angle	        -0.0 deg                -0.0 deg         	            ...
    ratio	        0.76948964274897        0.76948964274897              	...
    '''
    # set column
    column = ['min coordinate', 'max coordinate', 'vector', 'distance', 'angle', 'ratio']
    
    # get field arrow
    if self._ndim == 1:
      meta = {'unit':Unit('mm'), 't0':self.t0, 'datetime':self.datetime, 'field direction':self._axis, 'conduct model':self._conduct_model, 'eigenvalues':self._eigenvalues}
      info = self._get_pole_information(self)
      
      return QTable([column, info],
                    names=('type', self.t0), meta=meta)
    
    elif self._ndim == 2:
      _t0 = self.t0
      info = [column]
      names = ['type']
      meta = {'unit':Unit('mm'), 't0':self.t0, 'datetime':self.datetime, 'field direction':self._axis, 'conduct model':self._conduct_model, 'eigenvalues':self._eigenvalues}
      for n, epoch_data in enumerate(self):
        epoch = _t0 + (n*self.sample_rate.value)*second
        epoch_datetime = tconvert(epoch.value)
        info.append(self._get_pole_information(epoch_data))
        names.append(epoch)
      return QTable(info,
                    names=names, meta=meta)
  
  def plot(self, epoch, arrows=False, pole_arrow=False):
    '''it will be supported
    '''
    pass

