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
>>> kdf_path = '~/test/kdf/file.kdf'
>>> config_path = '~/test/config/file.ini'
>>> dataset = TimeSeriesArray(source=kdf_path, config=config_path)
>>> print(dataset)
<TimeSeriesArray [[  136.26813889,   156.58140182,   177.74105072, ...,
                    -140.50006866,   -67.71087646,    33.00905228],
                  [  455.35564423,   413.03634644,   386.79838181, ...,
                      70.25003433,    60.09340286,   143.03922653],
                  [  804.91304398,   845.53956985,   888.7052536 , ...,
                     571.31052017,   643.25332642,   461.28034592],
                  ...,
                  [-1409.23261642, -1286.50665283, -1270.42531967, ...,
                   -2376.65176392, -2374.958992  , -2407.96804428],
                  [-1499.7959137 , -1494.71759796, -1477.78987885, ...,
                   -1985.62145233, -1954.30517197, -1994.93169785],
                  [-2495.14579773, -2518.84460449, -2456.21204376, ...,
                   -1951.7660141 , -1929.75997925, -1776.56412125]] 1e-15 T>
```

```note
Since KDF format has a limited metadata container, an additional configuration `ini` file that comprises sensor information is required. 

See detailed explanation about `ini` file in [Data Tables](https://pjjung.github.io/mcgpy/MCGdata/Data_tables.html) section.
```

Alongside basic properties, this object also provides additional metadata:

| Properties  | Description                   |
|-------------|-------------------------------|
| `datetime`    | The data time at the point of data recording *i.e., '2020-02-02 02:02:02.00000'* |
| `biosemi`     | Identification code *i.e., National Hospital, National Reaserch, ...*|
| `note`        | It might be included with the patient information or medical options |

Every metadata can be redefined as well:

```python
>>> dataset.note = 'Phil is healthy'
>>> print(dataset.note)
'Phil is healthy'
```

### HDF5 format

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> hdf_path = '~/test/kdf/file.hdf5'
>>> dataset = TimeSeriesArray(hdf_path)
>>> print(dataset)
<TimeSeriesArray [[  136.26813889,   156.58140182,   177.74105072, ...,
                    -140.50006866,   -67.71087646,    33.00905228],
                  [  455.35564423,   413.03634644,   386.79838181, ...,
                      70.25003433,    60.09340286,   143.03922653],
                  [  804.91304398,   845.53956985,   888.7052536 , ...,
                     571.31052017,   643.25332642,   461.28034592],
                  ...,
                  [-1409.23261642, -1286.50665283, -1270.42531967, ...,
                   -2376.65176392, -2374.958992  , -2407.96804428],
                  [-1499.7959137 , -1494.71759796, -1477.78987885, ...,
                   -1985.62145233, -1954.30517197, -1994.93169785],
                  [-2495.14579773, -2518.84460449, -2456.21204376, ...,
                   -1951.7660141 , -1929.75997925, -1776.56412125]] 1e-15 T>
```

In the case of using an HDF5 file, you do not care about additional configuration files and metadata. Rest usages are the same as the above case.

## Associated classes

Note that in addition to the TimeSeires associated classes listed below.

| Classes             | Description                   |
|---------------------|-------------------------------|
| [TimeSeriesArray]() | Dealing with a multi-channel time-series array of a MCG dataset | 
| [TimeSeires]()      | Dealing with a single time-series of a MCG dataset |
| [ChannelActive]()   | Listing the channel status |
