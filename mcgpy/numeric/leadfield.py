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

'''leadfield : a utility to calculate lead field by sensor information, source and virtual planes.
'''

import numpy as np
from astropy.units import Quantity

__author__ = 'Phil Jung <pjjung@amcg.kr>'

class LeadField(np.ndarray):
  def __new__(cls, positions, directions,
              sourcegrid_width, sourcegrid_height, sourcegrid_interval,
              baseline=50, axis='z', conduct_model='horizontal', **kwargs):
    '''calculate lead field matrix
    
    Parameters
    ----------
    positions : "list", "tuple", "np.ndarray"
        the list of sensor's positions
    
    directions : "list", "tuple", "np.ndarray"
        the list of sensor's directions
    
    sourcegrid_width : "int", "float", "astropy.units.Quantity"
        width of source plane
        in case of source grid, defualt value is 240 [mm]
        in case of sensor grid, defualt value is 400 [mm]
    
    sourcegrid_height : "int", "float", "astropy.units.Quantity"
        height of source plane
        in case of source grid, defualt value is -40 [mm]
        in case of sensor grid, defualt value is 40 [mm]
    
    sourcegrid_interval : "int", "float", "astropy.units.Quantity"
        interval of source plane's cell
        in case of source grid, defualt value is 16 [mm]
        in case of sensor grid, defualt value is 25 [mm]
    
    baseline : "int", "float", "astropy.units.Quantity", optional
        length of baseline (Z-axis height of each sensor) 
    
    axis : "str", optional
        dipole axis on the grid
    
    conduct_model : "str", optional
        source grid conduct model
    
    Raises
    ------
    ValueError
        1) axis argument takes 'x', 'y', and 'z'
        2) conduct model takes 'spherical', 'horizontal', and 'free'
    
    Return : "mcgpy.LeadField"
    ------
        lead field matrix
    
    Note
    ----
    See the following articles for understanding theoretical backgrounds.
        M.S Hamalainen, et al., Interpreting magnetic fields of the brain: minimum orm estimates,  Med. & Biol. Eng. & Compu., 32, 35-42 (1994)
        J.T. Nenonen, et al., Minimum-norm estimation in a boundary-element torso model, Med. & Biol. Eng. & Compu., 32, 42-48 (1994)
    '''
    
    ## parameters
    cls._positions = positions
    cls._directions = directions
    cls._baseline = cls._get_value(baseline)
    cls._axis = axis
    cls._conduct_model = conduct_model
    
    # get lead field matrix
    new = cls._get_leadfield(sourcegrid_width, sourcegrid_height, sourcegrid_interval, cls._baseline).view(cls)

    return new
    
  ##---- Inherent functions -------------------------------- 
  @classmethod
  def _get_value(cls, value):
    if isinstance(value, Quantity):
      value = value.value
    return value
  
  @classmethod
  def _update_attribute(cls, key, value):
    _key = '_{}'.format(key)
    try:
      current_attribute = getattr(cls, _key)
      if (value is None
          or value != current_attribute
          or getattr(cls, key) is None):
        delattr(cls, _key)
        setattr(cls, _key, value)
    except (AttributeError, ValueError):
      setattr(cls, _key, value)

  @classmethod
  def _get_leadfield(cls, grid_width, grid_height, grid_interval, baseline, **kwargs):
    ## get source grid
    sourcegrid = cls._get_sourcegrid(width=grid_width, height=grid_height, interval=grid_interval)

    ## make dipole unit by the given axis
    if cls._axis == 'z':
      component_number = 2
      dipole_unit = np.delete(np.identity(3), 2, axis=0)
    elif cls._axis == 'x' or axis == 'y':
      component_number = 3
      dipole_unit = np.identity(3)
    else:
      raise ValueError('axis argument takes "x", "y", or "z", but irregular argument was given')

    ## make leadfield matrix  
    length = sourcegrid.shape[0]*component_number
    leadfield = np.zeros((length, length))
    for i, position in enumerate(cls._positions):
      direction = cls._directions[i]
      for j, cell in enumerate(sourcegrid):
        BB = cls._get_magnetic_vector(position, direction, cell, dipole_unit, baseline, cls._conduct_model)
        for k, B in enumerate(BB):
          leadfield[i, j*component_number+k] = B

    cls._update_attribute('component_number', component_number)
    cls._update_attribute('dipole_unit', dipole_unit)
    cls._update_attribute('sourcegrid', sourcegrid)
          
    return leadfield
  
  @classmethod
  def _get_virtural_leadfield(cls, grid_width, grid_height, grid_interval, direction='z', **kwargs):
    ## get virtual sensor grid as sensor positions
    positions = cls._get_sourcegrid(width=grid_width, height=grid_height, interval=grid_interval)
    
    ## make virtual sensor dirations
    directions = np.zeros((positions.shape))
    if direction == 'z':
      directions[:,2] = 1
    elif direction == 'y':
      directions[:,1] = 1
    elif direction == 'x':
      direction[:,0] = 1
    
    ## make leadfield matrix  
    length = cls._sourcegrid.shape[0]*cls._component_number
    leadfield = np.zeros((length, length))
    for i, position in enumerate(positions):
      direction = directions[i]
      for j, cell in enumerate(cls._sourcegrid):
        BB = cls._get_magnetic_vector(position, direction, cell, cls._dipole_unit, 0, cls._conduct_model)
        for k, B in enumerate(BB):
          leadfield[i, j*cls._component_number+k] = B

    return leadfield
  
  @classmethod
  def _get_sourcegrid(cls, width, height, interval, **kwargs):  
    width = cls._get_value(width)
    height = cls._get_value(height)
    interval = cls._get_value(interval)
    
    coordinate = np.arange(-0.5*width, 0.5*width+interval, interval)
    X, Y = np.meshgrid(coordinate, coordinate)
  
    return np.array([X.flatten(),  Y.flatten(), np.full(len(coordinate)**2, height)]).T

  @classmethod
  def _get_magnetic_vector(cls, position, direction, cell, dipole_unit, baseline, conduct_model, **kwargs):
    BB = np.zeros((len(dipole_unit)))
    for i, dipole in enumerate(dipole_unit):
      if baseline is None or baseline == 0:
        Bxyz = cls._get_Bxyz(position, cell, dipole, conduct_model)
        BB[i] = np.dot(Bxyz, np.abs(direction))
      else:
        Bxyz_top = cls._get_Bxyz(position+[0,0,baseline], cell, dipole, conduct_model)
        Bxyz_bottom = cls._get_Bxyz(position, cell, dipole, conduct_model)
        BB[i] = np.dot(Bxyz_bottom - Bxyz_top, direction)

    return BB

  @classmethod
  def _get_Bxyz(cls, position, cell, dipole, conduct_model, **kwargs):
    if conduct_model == 'spherical':
      x0, y0, z0 = cell
      x, y, z = position
      Qx, Qy, Qz = dipole

      r = np.sqrt(x**2 + y**2 + z**2)
      a = np.sqrt((x-x0)**2+(y-y0)**2+(z-z0)**2)
      ar=(x-x0)*x+(y-y0)*y+(z-z0)*z
      F=a*(r*a+r**2-(x*x0+y*y0+z*z0))
      dFx=x*(a**2/r+a)+(x-x0)*(a+2*r+ar/a)
      dFy=y*(a**2/r+a)+(y-y0)*(a+2*r+ar/a)
      dFz=z*(a**2/r+a)+(z-z0)*(a+2*r+ar/a)
      Qxr0r=(Qy*z0-Qz*y0)*x+(Qz*x0-Qx*z0)*y+(Qx*y0-Qy*x0)*z
      Bx=(Qy*z0-Qz*y0)/F-Qxr0r*dFx/F**2
      By=(Qz*x0-Qx*z0)/F-Qxr0r*dFy/F**2
      Bz=(Qx*y0-Qy*x0)/F-Qxr0r*dFz/F**2

      Bxyz = np.multiply(100000.0, [Bx, By, Bz])

    elif conduct_model == 'horizontal':
      x0, y0, z0 = cell
      x, y, z = position
      Qx, Qy, Qz = dipole

      a=np.sqrt((x-x0)**2+(y-y0)**2+(z-z0)**2)
      K=a*(a+z-z0)
      dKx=(x-x0)*(2+(z-z0)/a)
      dKy=(y-y0)*(2+(z-z0)/a)
      dKz=(z-z0)*(2+(z-z0)/a)+a
      Bx=Qy/K+(Qx*(y-y0)-Qy*(x-x0))*dKx/K**2
      By=-Qx/K+(Qx*(y-y0)-Qy*(x-x0))*dKy/K**2
      Bz=(Qx*(y-y0)-Qy*(x-x0))*dKz/K**2

      Bxyz = np.multiply(100000.0, [Bx, By, Bz])

    elif conduct_model == 'free':
      x0, y0, z0 = cell
      x, y, z = position
      Qx, Qy, Qz = dipole

      r=np.sqrt((x-x0)**2+(y-y0)**2+(z-z0)**2)
      Bx=(Qy*(z-z0)-Qz*(y-y0))/r**3
      By=(Qz*(x-x0)-Qx*(z-z0))/r**3
      Bz=(Qx*(y-y0)-Qy*(x-x0))/r**3

      Bxyz = np.multiply(100000.0, [Bx, By, Bz])

    else:
      raise ValueError('conduct_model argument takes "spherical", "horizontal", and "free", but irregular argument was given')

    return Bxyz  
  
  ##---- Methods --------------------------------
  # get inverse leadfield matrix
  def inverse(self, eigenvalues=10, **kwargs):
    '''calculate an inverse lead field matrix by using SVD method
    
    Parameters
    ----------
    eigenvalues : "int", optional
        the number of eigenvalues for SVD calculation,
        default value is 10
    
    Return : "np.ndarray"
    ------
        quasi-inverser lead field matrix
    '''
    
    ## reduce lead field matrix by active channels
    for i, row in enumerate(self):
      if i == 0:
        _leadfield = row
      elif i > 0 and np.sum(row) != 0:
        _leadfield = np.vstack((_leadfield, row))
    
    ## make diagonal norm matrix 
    diagonal_norm_matrix = np.zeros((_leadfield.shape[1], _leadfield.shape[1]))
    for i, row in enumerate(_leadfield.T):
      diagonal_norm_matrix[i,i] = np.sqrt(1/np.linalg.norm(row))

    ## calculate SVD
    special_matrix = np.dot(_leadfield, diagonal_norm_matrix)
    u, s, vh = np.linalg.svd(special_matrix, full_matrices=True)

    ## calculate inverse matrix
    if eigenvalues == 11:
      fractional_index = np.where(s[::-1] > np.multiply(np.sum(s), 0.01))[0][0]
      eigenvalues = s.shape[0] - np.int16(fractional_index) - 6

    b = np.dot(np.diag(1/s[:eigenvalues]), u[:,:eigenvalues].T)
    a = np.dot(vh.T[:,:eigenvalues], b)
    
    return np.dot(diagonal_norm_matrix, a)
    
    
  # magnetic vectors of x/y/z-axis on virtural sensor grid
  def field_map(self, data, sensorgrid_width, sensorgrid_height, sensorgrid_interval, eigenvalues=10, direction='z', **kwargs):
    '''calculate field map on Z-axis and meshgrid of X- and Y-axises
    
    Parameters
    ----------
    data : "mcgpy.timeseriesarray.TimeSeriesArray" 
        MCG dataset at the certain time
    
    sensorgrid_width : "int",  "float", "astropy.units.Quantity"
        width of sensor plane
    
    sensorgrid_height : "int",  "float", "astropy.units.Quantity"
        hieght of sensor plane
    
    sensorgrid_interval : "int",  "float", "astropy.units.Quantity"
        interval of sensor plane's cell
    
    eigenvalues : "int"
        the number of eigenvalues to get the inverser lead field matrix
    
    direction : "str"
        magnetic vector direction on the sensor plane
        default value is Z-axis
    
    Raises
    ------
    TypeError
        if input data is not one-dimentional array
    
    Return : "tuple"
    ------
    X
         x-axis meshgrid
    Y
         y-axis meshgrid
    Z
         magnitude of amplitude vector on sensor plane
    
    '''
    
    ## given data check
    data = self._get_value(data)
    if not np.ndim(data) == 1:
      raise TypeError('data takes one-dimensional array, but {} was given'.format(np.ndim(data)))
    
    ## get inverse lead field matrix
    inverse_leadfield = self.inverse(eigenvalues)
    
    ## get virtual lead field matrix
    virtual_leadfield = self._get_virtural_leadfield(sensorgrid_width, sensorgrid_height, sensorgrid_interval, direction)
    
    ## get map coordinate
    coordinate = np.arange(-0.5*sensorgrid_width, 0.5*sensorgrid_width+sensorgrid_interval, sensorgrid_interval)

    ## calculate magnetic field mapt on z-direction
    A = np.dot(inverse_leadfield, data)
    Bz = np.dot(virtual_leadfield, A)
    Z = Bz[:len(coordinate)**2].reshape(len(coordinate), len(coordinate))
    X, Y = np.meshgrid(coordinate, coordinate)
    
    return X, Y, Z
    
