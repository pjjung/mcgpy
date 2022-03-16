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

The syntax is follows as below:

```ini
[Label]
1 = label_1
2 = label_2
3 = label_3

[Positions]
1 = 10.000, 10.000,   0.000
2 = 10.000, 15.000,   0.000
# = 10.000, 20.000,   0.000

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

```python
>>> from mcgpy.channel import ChannelActive
```

bla bla

## FieldMap

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> from mcgpy.numeric import FieldMap
```

### `FieldMap.arrows()`

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> from mcgpy.numeric import FieldMap
```

### `FieldMap.pole()`



## Accosicated classes

Note that in addition to the TimeSeires associated classes listed below.

| Classes             | Description                   |
|---------------------|-------------------------------|
| [TimeSeriesArray]() | Dealing with a multi-channel time-series array of a MCG dataset | 
| [TimeSeires]()      | Dealing with a single time-series of a MCG dataset |
| [Channel]()         | Listing the channel information from a configuration file or a raw frame file |
| [FieldMap]()        | Calculate a lead field matrix and the current-dipole information |
  
