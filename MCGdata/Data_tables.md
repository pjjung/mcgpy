---
sort: 3
---

# Data Tables

MCGpy provides `Data Tabels` to store sensor information and time-varying current dipole activities. Every table is built as an [astropy.table](https://docs.astropy.org/en/stable/table/index.html) object. Then, users can easily modify and deal with elements. 

This page shows two common examples when users encounter the situations `Data Tables` are required.

## The Channel

```python
from mcgpy.channel import (ChannelConfig, ChannelActive)
```

`Channel` module consists of [ChannelConfig]() and [ChannelActive]() classes. Each one has a function to read sensor information from the `ini` configuration file and from frame files, respectively.

### The ChannelConfig

Magnetocardiography (MCG) data analysis is performed by not only time-varying magnetic signals also field distributions. In the case of reading a frame file that only included time-series datasets without sensor information, this configuration file is significant.

The syntax of a sensor configuration `ini` file is follows as below:

```ini
[Label]
1 = label_1
2 = label_2
3 = label_3

[Positions]
1 = 10.000, 10.000,   0.000
2 = 10.000, 15.000,   0.000
3 = 10.000, 20.000,   0.000

[Directions]
1 = 1.0000,  0.0000,  0.0000
2 = 1.0000,  0.0000,  0.0000
3 = 1.0000,  0.0000,  0.0000
```

There are examples of how to read sensor information from an `ini` file.


```python
>>> from mcgpy.channel import ChannelConfig
>>> ini_path = '~/test/config/file.ini'
>>> config = ChannelConfig(ini_path)
>>> config.get('label')    # get the label list of sensors
    number	label
    int64	str3
    1	    label_1
    2	    label_2
    3	    label_3
    
>>> config.get('positions')    # get the position list of sensors
    number	positions
    int64	float64
    1	    (10., 10., 0.)
    2	    (10., 15., 0.)
    3	    (10., 20., 0.)

>>> config.get('directions')    # get the directions list of sensors
    number	positions
    int64	float64
    1	    (1.,  0.,  0.)
    2	    (1.,  0.,  0.)
    3	    (1.,  0.,  0.)
```

### The ChannelActive

This class has a function to extract channel numbers and labels from a frame file. It will be useful when users want to read a single time series by using [TimeSeires]() class, but the channel's number or label is unknown.


There are examples of how to obtain sensor's numbers and labels.

```python
>>> from mcgpy.channel import ChannelActive
>>> kdf_path = '~/test/raw/file.kdf'
>>> ch_info = ChannelActive(kdf_path)
>>> ch_info.get_table()    # obtain channel number and label as the table
    number	label
    int64	str3
    1	    label_1
    2	    label_2
    4	    label_4
    10	    label_10
    11	    label_11
    .
    .  
    
>>> ch_info.get_number()    # obtain channel numbers as the list
[1,2,4,10,11,...]
>>> ch_info.get_label()     # obtain channel labels as the list
['label_1','label_2','label_4','label_10','label_11',...]
```

## FieldMap

Although a contour map, like the magnetic field map at a certain time of the MCG dataset, is a scalar dataset. By calculating the gradient on each point or cell, vector distribution map can be obtained. However, it is hard to organize them into a simple matrix, for vectors are represented by their magnitude and direction on the coordinate system. Therefore, current arrows are stored as the table.

There are two examples of current arrows and the field pole arrow with `arrows()` and `pole()` methods, respectively.

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> from mcgpy.numeric import FieldMap
>>> hdf_path = '~/test/raw/file.hdf5'
>>> epoch_dataset = TimeSeriesArray(hdf_path).at(1126259462)
>>> fieldmap = FieldMap(epoch_dataset)
>>>
>>> fieldmap.arrows()     # get the arrow information
    tails 	              heads	                 vectors	    distances
    float64	              float64	             complex128	    float64
    (-200.0,0.0,-200.0)	  (-200.13,0.0,-200.15)	(-0.13-0.15j) 	0.20
    (-175.0,0.0,-200.0)	  (-175.18,0.0,-200.17)	(-0.18-0.17j)  	0.25
    .
    .
    .
    
>>>
>>> fieldmap.pole()       # get the field pole information
    type         	1126259462 s
    str14        	object
    min coordinate	(-75.0, -100.0)
    max coordinate	(75.0, 100.0)
    vector	        (150+0j)
    distance	    150.0
    angle	        -0.0 deg
    ratio	        0.76948964274897
```

## Accosicated classes

Note that in addition to the TimeSeires associated classes listed below.

| Classes             | Description                   |
|---------------------|-------------------------------|
| [TimeSeriesArray]() | Dealing with a multi-channel time-series array of a MCG dataset | 
| [TimeSeires]()      | Dealing with a single time-series of a MCG dataset |
| [Channel]()         | Listing the channel information from a configuration file or a raw frame file |
| [FieldMap]()        | Calculate a lead field matrix and the current-dipole information |
  
