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
asd

```


```python
>>> from mcgpy.channel import ChannelConfig
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
  
