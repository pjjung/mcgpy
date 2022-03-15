---
sort: 2
---

# Time Series Array Data
 

## The TimeSeriesArray

```python
from mcgpy.timeseriesarray import TimeSeriesArray
```
MCGpy also provide the [TimeSeriesArray]() class which create the time-series array with metadata and reads a multi-channel dataset from raw files. Since this object is based on [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html) and [astropy.units.Quantity](https://docs.astropy.org/en/stable/units/quantity.html), [numpy](https://numpy.org/) and [astropy](https://www.astropy.org/) users might be easy to learn how to use it.

There are the available source formats:

| Format  | Read     | Write     | Auto identify     | 
| ------- | -------- | --------- | ----------------- | 
| KDF     | Yes      | No        | Yes               |
| HDF5    | Yes      | will be supported| Yes        |

> The KDF is a multi-channel data format for the magnetocardiography system. It is based on [the BioSemi Data Format](https://www.biosemi.com/faq/file_format.htm), for BDF format is mainly used in the reseaches of electrocardiogram(ECG) and electroencephalography(EEG).
> 
> [The HDF5 format](https://www.hdfgroup.org/solutions/hdf5/) is high-performance data management and storage suite. Thanks to its flexibility and capability, multi-array dataset like MCG datasets can easily be handled. 

For examples, to create a simple [TimeSeriesArray]() by a ramdom dataset, and to read a multi-channel dataset from a frame file:

### User defined dataset

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> import numpy as np
>>> source = np.random.random((10,100))    # (channels, data points)
>>> positions = np.random.random((10,3))   # (channels, coordinates) i.e., [[0.,0.,0.], [1.,0.,0.], ...]
>>> directions = np.vander(np.linspace(0,0,10),3)    # (channels, vectors) i.e., [[0,0,1], [0,0,1], ...]
>>> dataset = TimeSeriesArray(source=source, positions=positions, directions=directions)
>>> print(dataset)
<TimeSeriesArray [[0.72475969, 0.19941436, ..., 0.82408383],
                  [0.94124398, 0.59067703, ..., 0.536895  ],
                  ...,
                  [0.56051709, 0.9914608 , ..., 0.29988421]] 1e-15 T>
```

Unlike the [TimeSeries]() class, [TimeSeriesArray]() class requires, not only the source array also position and direction information of each sensor if you apply your own dataset to MCGpy. This is because these sensor data are essential to calculate `Field Map`, `MCG mapping`, `Locations of current sources`, and so on.

[TimeSeriesArray]() contains several properties to show metadata:
 
| Properties    | Description                   |
|---------------|-------------------------------|
| `unit`        | The physical unit of the data, default unit is $$1 fT$$ |
| `t0`          | The first data point of time-axis, default value is $$0 s$$ |
| `dt`          | The inderval bwteen time points of time-axis, default value is $$1 s$$ |
| `sample_rate` | Data sample frequency, default value is $$1 Hz$$ |
| `times`       | The time-axis coordinate |
| `numbers`     | Number of channels *i.e., [1, 2, 3, ...]*|
| `labels`      | Label of channels *i.e., [label1, label2, label3, ...]*|
| `positions`   | Positions of each sensor *i.e., [[0.,0.,0.], [1.,0.,0.], ...]* |
| `directions`  | Directions of each sensor *i.e., [[0,0,1], [0,0,1], ...]* |

### KDF format

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
```
bla bla


### HDF5 format

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
```
bla bla


## Associated classes

Note that in addition to the TimeSeires associated classes listed below.

| Classes             | Description                   |
|---------------------|-------------------------------|
| [TimeSeriesArray]() | Dealing with a multi-channel time-series array of a MCG dataset | 
| [TimeSeires]()      | Dealing with a single time-series of a MCG dataset |
| [ChannelActive]()   | Listing the channel status |
| [tconvert]()        | Convert a date time string to a timestamp, or vice versa |
