---
sort: 2
---

# TimeSeriesArray

*class* **mcgpy.timeseriesarray.TimeSeriesArray**(source, config=None, positions=None, directions=None, unit=None, t0=None, sample_rate=None, times=None, **kwargs)

Make a multi-channel time-series array with metadata

## Parameters

* **source** : `str`, `list`, `np.ndarray`, `astropy.units.Quantity`, `mcgpy.io.Array`

  it can take multi-type data formats

* **config** : `str`, conditional

  if the input source is the KDF file path,
  this parameter is essential

* **positions** : `list`, `np.ndarray`, `astropy.units.Quantity`, optional

  sensor positions
  * if the input source is the KDF file path and sensor configuration file path is also given,
    this parameter will be ignored
  * if the input source is the HDF file path,
    this parameter will be ignored
  * if the input source is user defined data array and will not use numerical classes, `mcgpy.numeric.LeadField` and `mcgpy.numeric.FieldMap`,
    this parameter is optional

* **directions** : `list`, `np.ndarray`, `astropy.units.Quantity`, optional

  sensor positions
  * if the input source is the KDF file path and sensor configuration file path is also given,
    this parameter will be ignored
  * if the input source is the HDF file path,
    this parameter will be ignored
  * if the input source is user defined data array and will not use numerical classes, `mcgpy.numeric.LeadField` and `mcgpy.numeric.FieldMap`,
    this parameter is optional

* **unit** : `astropy.units.Quantity`, optional

  an unit of data,

  default unit is femto tesla, 10E-15 T, if the input source is not KDF or HDF5 file path

* **t0** : `int`, `float`, `astropy.units.Quantity`, optional

  start time of time-series,

  default value is 0 s, if the input source is not KDF or HDF5 file path

* **sample_rate** : `int`, `float`, `astropy.units.Quantity`, optional

  signal sample frequency,

  default value is 1 Hz, if the input source is not KDF or HDF5 file path

* **times** : `list`, `np.ndarray`, `astropy.units.Quantity`, optional

  time xindex,
  
  default value is made by data size, t0 and sample_rate, if the input source is not KDF or HDF5 file path

## Return

* if the input source is the path of a KDF or HDF5 file,
  read whole dataset and return it with metadata.
           
* if the input source is the data array,
  read a data of given channel number or label, and return it.

  return the time-series array with metadata

## Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
>>> dataset
[[136.26814, 156.5814, …, −67.710876, 33.009052], 
[455.35564, 413.03635, …, 60.093403, 143.03923],
…, 
[−1409.2326, −1286.5067,  …, −2374.959, −2407.968], 
[−1499.7959, −1494.7176,  …,  −1954.3052, −1994.9317]]1×10−15T
>>> dataset.directions
array([[1., 0., 0.],
      [1., 0., 0.],
       ...,
      [0., 1., 0.],
      [0., 1., 0.]])
    
```

```note
this class is designed to apply to numerical classes with a multi-channel time-series of MCG system, though.

user defined data array can be applied, and use its properties and methods, too.
```

## Properties Summary

| Properties     | Discription |
|----------------|-------------|
| [biosemo](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#biosemi)      | Identification code         |
| [channels](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#channels)      | Channel information table of numbers and labels        |
| [datetime](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#datetime)    | The data time at the point of data recording         |
| [direction](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#direction)  | The sensor direction for measuring a magnetic field if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional        |
| [directions](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#directions)  | The sensor directions for measuring magnetic fields if `mcgpy.timeseriesarray.TimeSeriesArray` is two-dimentaional       |
| [duration](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#duration)    | Data recording duration        |
| [label](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#label)          | Label of a channel magnetic field if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional          |
| [labels](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#labels)          | Labels of channel magnetic fields if `mcgpy.timeseriesarray.TimeSeriesArray` is two-dimentaional          |
| [note](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#note)            | It might be included with the patient information or medical options          |
| [number](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#number)        | Number of a channel magnetic field if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional         |
| [numbers](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#numbers)        | Numbers of channel magnetic fields if `mcgpy.timeseriesarray.TimeSeriesArray` is two-dimentaional         |
| [position](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#position)    | The sensor direction for measuring a magnetic field  if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional          |
| [positions](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#positions)    | The sensor directions for measuring magnetic fields  if `mcgpy.timeseriesarray.TimeSeriesArray` is two-dimentaional          |
| [sample_rate](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#sample_rate)| Data sample frequency         |
| [t0](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#t0)| The first data point of time-axis        |
| [times](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#times)| The time-axis coordinate         |
| [unit](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#unit)| The physical unit of the data         |

## Methods Summary

| Methods        | Discription |
|----------------|-------------|
| [area(start, end)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#areastart-end-kwargs)           |    Calculate the area between start and end timestamps         |
| [asd(fftlength, overlap, window, average)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#asdfftlengthnone-overlap0-windowhann-averagemedian-kwargs)           |   Calculate the acceleration spectral density, ASD          |
| [at(epoch)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#atepoch-kwargs)           |  Peak up the value/values at an input time           |
| [bandpass(lfreq, hfreq)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#bandpasslfreq-hfreq-order4-kwargs)           |  Apply the bandpass filter to the dataset           |
| [crop(start, end)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#cropstart-end-kwargs)           |  Slice the time-series between start and end times        |
| [exclude(numbers, labels)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#excludenumbersnone-labelsnone-kwargs)           |    Except the channel data from the dataset         |
| [fft()](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#fft)           |    Calculate the fast Fourier transform, FFT         |
| [flattened(freq)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#flattenedfreq1-kwargs) | Flatten a wave-form by a lowpass filter |
| [highpass(hfreq, order)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#highpasshfreq-order2-kwargs)           |   Apply the highpass filter to the dataset         |
| [integral(start, end)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#integralstart-end-kwargs)           |  Calculate the integrated area between start and end timestamps           |
| [lowpass(lfreq, order)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#lowpasslfreq-order2-kwargs)           |   Apply the lowpass filter to the dataset          |
| [notch(freq, Q)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#notchfreq-q30-kwargs)           |  Apply the notch/bandstop filter to the dataset          |
| [offset_correction(interval)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#offset_correctioninterval2-kwargs)           |   Offset correction by signal mode value          |
| [offset_correction_at(epoch)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#offset_correction_atepoch-kwargs)           |    Offset correction by the value at the given timestamp, each signal offset will be subtracted from the value at the given timestamp         |
| [psd(fftlength, overlap, window, average)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#psdfftlengthnone-overlap0-windowhann-averagemedian-kwargs)           |   Calculate the power spectral density, PSD          |
| [read(number, label)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#readnumbernone-labelnone-kwargs)           |   Read one channel data from the dataset          |
| [rms(stride)](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#rmsstride1-kwargs)           |    Get the rms dataset by a given stride  |
| [to_avg()](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#to_avg)           |    Calculate an average of channel signals         |
| [to_rms()](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#to_rms)           |    Calculate the rms for all channels         |


## Properties Documentation

#### biosemi

Identification code _i.e., National Hospital, National Reaserch, …_

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.biosemi)
'MCGpy schoool'
```

---
#### channels 

Channel information table of numbers and labels

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.channels)
<QTable length=8>
number label
int64   str3
------ -----
     1    label_1
     2    label_2
     3    label_3
     4    label_4
     5    label_5
     6    label_6
     7    label_7
     8    label_8
```
#### datetime 

The data time at the point of data recording_ i.e., ‘2020-02-02 02:02:02.00000'_

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.datetime)
'2020-02-02 02:02:02'
```
---
#### direction

The sensor direction for measuring a magnetic field _i.e., [1.,0.,0.]_
if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> ch1 = dateset.read(number=1)
>>> print(ch1.direction)
array([1, 0, 0])
```
---
#### directions

The sensor direction for measuring a magnetic field _i.e., [[1.,0.,0.],[1.,0.,0.],...,[0.,1.,0.]]_
if `mcgpy.timeseriesarray.TimeSeriesArray` is two-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.directions)
array([[1., 0., 0.],
       [1., 0., 0.],
       [1., 0., 0.],
       [1., 0., 0.],
       [0., 1., 0.],
       [0., 1., 0.],
       [0., 1., 0.],
       [0., 1., 0.]]
```
---
#### duration 

Data recording duration

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.duration)
<Quantity 10. s>
```
---
#### label

Label of a channel magnetic field if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> ch1 = dateset.read(number=1)
>>> print(ch1.label)
'label_1'
```
---
#### labels

Labels of channel magnetic fields if `mcgpy.timeseriesarray.TimeSeriesArray` is two-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.labels)
array(['label_1', 'label_2', 'label_3', 'label_4', 'label_5', 'label_6', 'label_7', 'label_8'], dtype='<U3')
```
#### note

It might be included with the patient information or medical options.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.note)
{'encoded info': 'a7F76ae32B2566A8F165_22221223',
 'opinion': 'Healthy',
 'patient number': '0000'}
```
---
#### number

Number of a channel magnetic field if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> ch1 = dateset.read(number=1)
>>> print(ch1.number)
1

```
#### numbers

Numbers of channel magnetic fields if `mcgpy.timeseriesarray.TimeSeriesArray` is two-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.numbers)
array([ 1,  2,  3,  4,  5,  6,  7,  8])
```
---
### position

The sensor direction for measuring a magnetic field if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> ch1 = dateset.read(number=1)
>>> print(ch1.position)
array([0, 0, 0])
```
---
### positions

The sensor directions for measuring magnetic fields if `mcgpy.timeseriesarray.TimeSeriesArray` is two-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.positions)
array([[  10.  ,  0.,    0.   ],
       [  -10. ,  0.,    0.   ],
       [  0.   ,  10.,   0.   ],
       [  0.   , -10.,   0.   ],
       [  10.  ,  10 ,   0.   ],
       [  -10. , -10.,   0.   ],
       [  10.  , -10.,   0.   ],
       [  -10. ,  10.,   0.   ]])
```
#### sample_rate

Data sample frequency.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.sampe_rate)
<Quantity 1024 Hz>
```
---
#### t0

The first data point of time-axis.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.t0)
<Quantity 2082875272. s>
```
---
#### times

The time-axis coordinate.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.times)
<Quantity [1.08287527e+09, 1.08287527e+09, ...,1.08287528e+09] s>
```
---
#### unit

The physical unit of the data.

Here is an example:

```python
>>> from mcgpy.timeserie import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.unit)
Unit("1e-15 T")
```
---


## Methods Documentation

#### area(start, end, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.area(start, end, **kwargs)

Calculate the area between start and end timestamps.

#### Parameters

* start : `int`, `float`, `astropy.units.Quantity`

  start timestamp
    
* end : `int`, `float`, `astropy.units.Quantity`

  end timestamp

#### Return : `mcgpy.timeseries.TimeSeriesArray`

* if the dataset is one-dimensional,
  return the area of signal between start and end timestamps

* if the dateset is two-dimensional,
  return the area of signal between start and end timestamps for each channel

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.area(2082875272,2082875274)
[0.24546295, 0.46202301, ..., 1.409447, 2.6042676](𝑈𝑛𝑖𝑡𝑛𝑜𝑡𝑖𝑛𝑖𝑡𝑖𝑎𝑙𝑖𝑠𝑒𝑑)
```

---
#### asd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.asd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)

Calculate the acceleration spectral density, ASD

#### Parameters

* **fftlength** : `int`,  `float`, optional

  number of seconds for dividing the time window into equal bins,
  if None type value is given, it will be the size of signal

* **overlap** : `int`,  `float`, optional

  number of seconds of overlap between FFTs,
  default value is 0

* **window** : `str`

  Desired window to use. If window is a string or tuple, it is passed to get_window to generate the window values, 
  which are DFT-even by default. See get_window for a list of windows and required parameters. 
  If window is array_like it will be used directly as the window and its length must be nperseg. 
  Defaults to a Hann window.
  
  See more detailed explanation in [scipy.signal.welch](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)

* **average** : { "mean", "median" }, optional

  Method to use when averaging periodograms. 
  Defaults to ‘mean’.
  
  See more detailed explanation in [scipy.signal.welch](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)

#### Return : `mcgpy.series.FrequencySeries`

* if the dataset is one-dimensional,
  return asd frequency-series

* if the dateset is two-dimensional,
  return asd frequency-series for each channel
    
#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.asd(2,1)
[[16.390747, 62.977136, 149.35229, …, 1.8138222, 1.4555211, 0.93069027], 
[24.143041, 113.88421, 261.50669, …, 1.7955032, 1.8442637, 0.72403336], 
…, 
[12.476006, 44.834316, 56.699417, …, 1.6649341, 1.9098386, 1.0112418], 
[153.54132, 400.77368, 220.70556, …, 1.955279, 1.9509556, 0.80185085]]1×10−15THz1/2
```

---
#### at(epoch, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.at(epoch, **kwargs)

Peak up the value/values at an input time.

#### Parameters

* **epoch** : `int`, `float`, `astropy.units.Quantity`

  timestamp user wants to get the value

#### Return : `mcgpy.timeseries.TimeSeriesArray`

* if the dataset is one-dimensional,
  return the value at the given time

* if the dateset is two-dimensional,
  return the values for each channel at the given time

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.at(2082875272)
[136.26814, 455.35564, ..., −1499.7959, −2495.1458]1×10−15T
```

---
#### bandpass(lfreq, hfreq, order=4, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.bandpass(lfreq, hfreq, order=4, flattening=True, **kwargs)

Apply the bandpass filter to the dataset.

#### Parameters

* **lfreq** : `int`, `float`, `astropy.units.Quantity`

  the low cutoff frequencies 

* **hfreq** : `int`, `float`, `astropy.units.Quantity`

  the high cutoff frequencies 

* **sample_rate** : `int`, `float`, `astropy.units.Quantity`

  sample rate of ditital signal

* **order** : `int`, optional

  the order of the filter, default value is 4
    
* **flattening** : `Boonlean`, optional

  signal flattening option, defaule value is True
    
#### Return : `mcgpy.timeseries.TimeSeriesArray`

filted dataset

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.bandpass(0.1, 200)
    [[5.8798634, 35.303578, 95.930749, …, 72.160133, 27.332395, 18.921922], 
     [19.648239, 113.21599, 288.53974, …, 214.44662, 209.56741, 173.21204], 
     …, 
     [−64.715018, −378.69255, −987.28802, …, −195.79194, −150.83508, −97.942407], 
     [−107.66359, −631.4016, −1649.1429, …, −1785.628, −1803.213, −1788.7173]]1×10−15T
```

---
#### crop(start, end, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.crop(start, end, **kwargs)

Slice the time-series between start and end times.

#### Parameters

* **start** : `int`, `float`, `astropy.units.Quantity`

 start timestamp
    
* **end** : `int`, `float`, `astropy.units.Quantity`

 end timestamp
    
#### Return : `mcgpy.timeseries.TimeSeriesArray`

* if the dataset is one-dimensional,
  return sliced time-series array
           
* if the dateset is two-dimensional,
  return sliced time-series for each channel array

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.crop(2082875272,2082875273)
[[136.26814, 156.5814, 177.74105, …, 10.156631, −3.3855438, 5.9247017], 
 [455.35564, 413.03635, 386.79838, …, 394.41586, 352.94294, 360.56042], 
 …, 
 [−1499.7959, −1494.7176, −1477.7899, …, −1535.3441, −1401.6151, −1513.3381], 
 [−2495.1458, −2518.8446, −2456.212, …, −2870.9412, −2869.2484, −2865.0165]]1×10−15T
```

---
#### exclude(numbers=None, labels=None, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.exclude(numbers=None, labels=None, **kwargs)

Except the channel data from the dataset.

#### Parameters

* **numbers** : `list`, `tuple`, `np.ndarray`, conditional

  the number list of what user wants to remove channels from the dataset
    
* **labels** : `list`, `tuple`, `np.ndarray`, conditional

  the label list of what user wants to remove channels from the dataset
    
#### Return : `mcgpy.timeseries.TimeSeriesArray`

the dataset except for the given channel list

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.exclude(numbers=(1,2))
[[485.82554, 424.03936, 330.93691, …, 534.91592, 451.9701, 475.66891], 
 [214.13565, 215.82842, 265.76519, …, 275.92182, 276.76821, 246.29831], 
 …, 
 [−1499.7959, −1494.7176, −1477.7899, …, −1985.6215, −1954.3052, −1994.9317], 
 [−2495.1458, −2518.8446, −2456.212, …, −1951.766, −1929.76, −1776.5641]]1×10−15T
```

---
#### fft()

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.fft()

Calculate the fast Fourier transform, FFT.

#### Return : `mcgpy.series.FrequencySeries`

* if the dataset is one-dimensional,
  return fft frequency-series
           
* if the dateset is two-dimensional,
  return fft frequency-series for each channel

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.fft()
[[92.382265, 16.48454, 57.167697, …, 0.05992157, 0.27365534, 0.2273498], 
 [56.252973, 42.362682, 35.193567, …, 0.13228269, 0.017953475, 0.036300067], 
 …,  
 [1741.4278, 104.75867, 48.947051, …, 0.1638588, 0.14912128, 0.073103484], 
 [1630.1735, 103.73168, 145.30199, …, 0.10946647, 0.048501745, 0.073445149]]1×10−15T
```

---
#### flattened(freq=1, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.flattened(freq=1, **kwargs)

Flattened a wave form by a lowpass filter

#### Parameters

* freq : `int`, `float`, `astropy.units.Quantity`

  the frequency for the lowpass filter

#### Return : `mcgpy.series.TimeSeriesArray`

(original signal) - (lowpass filtered signal)

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> data = TimeSeriesArray("~/test/raw/file/path.hdf5")
>>> data.flattened()
[[−106.09462, −86.757371, …,−44.093128, −34.719921], [−101.92919, −147.60086, …,  −10.727882, −15.01086], 
 …, 
 [−26.580124, 33.935216,  …, 0.5097395, 0.65614824], 
 [37.148019, 35.133146, …, 22.03233, 31.360074]]1×10−15T
```

#### highpass(hfreq, order=2, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.highpass(hfreq, order=2, flattening=True, **kwargs)

Apply the highpass filter to the dataset.

#### Parameters

* **hfreq** : `int`, `float`, `astropy.units.Quantity`

  the cutoff frequencies 

* **sample_rate** : `int`, `float`, `astropy.units.Quantity`

  sample rate of ditital signal

* **order** : `int`, optional

  the order of the filter, default value is 2

* **flattening** : `Boonlean`, optional

  signal flattening option, defaule value is True

#### Return : `mcgpy.timeseries.TimeSeriesArray`

filted dataset

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.highpass(1)
[[135.67819, 154.72616, 174.44649, …, −63.927263, 8.7490505, 108.60693], 
 [453.38425, 407.31395, 377.63813, …, 83.275947, 71.758854, 153.03796], 
 …, 
 [−1493.3028, −1475.2884, −1445.5762, …, 5.3016175, 36.47909, −4.2455184], 
 [−2484.3434, −2486.3819, −2402.3519, …, −128.50984, −103.82009, 51.282091]]1×10−15T
```

---
#### integral(start, end, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.integral(start, end, **kwargs)

Calculate the integrated area between start and end timestamps.

#### Parameters

* start : `int`, `float`, `astropy.units.Quantity`

  start timestamp
    
* end : `int`, `float`, `astropy.units.Quantity`

  end timestamp

#### Return :`mcgpy.timeseries.TimeSeriesArray`

* if the dataset is one-dimensional,
  return the integrated area between start and end timestamps
           
* if the dateset is two-dimensional,
  return the integrated area between start and end timestamps for each channel

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.intergral(2082875272,2082875276)
[0.057181275, 0.18835077, ..., −1.409359, −2.5957822](𝑈𝑛𝑖𝑡𝑛𝑜𝑡𝑖𝑛𝑖𝑡𝑖𝑎𝑙𝑖𝑠𝑒𝑑)
```

---
#### lowpass(lfreq, order=2, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.lowpass(lfreq, order=2, flattening=True, **kwargs)

Apply the lowpass filter to the dataset.

#### Parameters
****
* lfreq : `int`, `float`, `astropy.units.Quantity`

  the cutoff frequencies 

* **sample_rate** : `int`, `float`, `astropy.units.Quantity`

  sample rate of ditital signal

* **order** : `int`, optional

  the order of the filter, default value is 2

* **flattening** : `Boonlean`, optional

  signal flattening option, defaule value is True

#### Return : `mcgpy.timeseries.TimeSeriesArray`

filted dataset

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.lowpass(300)
[[27.122792, 96.382285, 158.37537, …, −114.89549, −122.86079, −74.991527], 
 [90.633926, 300.13861, 435.25997, …, 125.62341, 87.47646, 76.55231], 
 …, 
 [−298.51918, −1015.2932, −1538.4497, …, −2075.8569, −2023.2914, −1972.1399], 
 [−496.63348, −1695.4982, −2574.3753, …, −1975.7265, −1958.595, −1906.0884]]1×10−15T
```

---
#### notch(freq, Q=30, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.notch(freq, Q=30, flattening=True, **kwargs)

Apply the notch/bandstop filter to the dataset.

#### Parameters

* **freq** : `int`, `float`, `astropy.units.Quantity`

  the cutoff frequencies 

* **sample_rate** : `int`, `float`, `astropy.units.Quantity`

  sample rate of ditital signal

* **Q** : `int`, optional

  the Q-factor of the filter, default value is 30

* **flattening** : `Boonlean`, optional

  signal flattening option, defaule value is True

#### Return : `mcgpy.timeseries.TimeSeriesArray`

filted dataset

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.notch(60)
[[135.4371, 154.08522, 173.6796, …, −134.07926, −57.510631, 44.525834], 
 [452.57862, 405.36713, 375.73626, …, 58.700064, 45.456142, 126.85806], 
 …, 
 [−1490.6493, −1468.6386, −1438.5928, …, −1970.1784, −1950.0809, −2002.2954], 
 [−2479.929, −2475.262, −2390.6521, …, −1948.1221, −1940.4119, −1800.9872]]1×10−15T
```

---
#### offset_correction(interval=2, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.offset_correction(interval=2, **kwargs)

Offset correction by signal mode value.

#### Parameters

* **interval** : `int`

  number of seconds for dividing the time-series

#### Return : `mcgpy.timeseries.TimeSeriesArray`

offset corrected dataset for each channel based on the signal mode value

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.offset_correction()
[[165.89165, 186.20491, 207.36456, …, −110.87656, −38.087368, 62.632561], 
 [236.98807, 194.66877, 168.43081, …, −148.11754, −158.27417, −75.32835], 
 …, 
 [514.60266, 519.68098, 536.6087, …, 28.777122, 60.093403, 19.466877], 
 [55.015087, 31.31628, 93.948841, …, 598.39487, 620.40091, 773.59676]]1×10−15T
```

```note
 [scipy.stats.mode](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html) is utilized to match the baseline of multi-channels, in which the mode is the modal (most common) value in the passed array.
```

---
#### offset_correction_at(epoch, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.offset_correction_at(epoch, **kwargs)

Offset correction by the value at the given timestamp, each signal offset will be subtracted from the value at the given timestamp.
    
#### Parameters

* **epoch** : `int`, `float`, `astropy.units.Quantity`

  timestamp user wants to get the value

#### Return : `mcgpy.timeseries.TimeSeriesArray`

offset corrected dataset for each channel based on the value of the input timestamp

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.offset_correction_at(2082875273.397583)
[[165.04526, 185.35852, 206.51817, …, −111.72295, −38.933754, 61.786175], 
 [27.084351, −15.234947, −41.472912, …, −358.02126, −368.17789, −285.23207], 
 …, 
 [−11.849403, −6.7710876, 10.156631, …, −497.67494, −466.35866, −506.98519], 
 [323.31944, 299.62063, 362.25319, …, 866.69922, 888.70525, 1041.9011]]1×10−15T
```

---
#### psd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.psd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)

Calculate the power spectral density, PSD.

#### Parameters

* **fftlength** : `int`,  `float`, optional

  number of seconds for dividing the time window into equal bins,
  if None type value is given, it will be the size of signal

* **overlap** : `int`,  `float`, optional

  number of seconds of overlap between FFTs,
  default value is 0

* **window** : `str`

  Desired window to use. If window is a string or tuple, it is passed to get_window to generate the window values, 
  which are DFT-even by default. See get_window for a list of windows and required parameters. 
  If window is array_like it will be used directly as the window and its length must be nperseg. 
  Defaults to a Hann window.

  See more detailed explanation in [scipy.signal.welch](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)

* **average** : { "mean", "median" }, optional

  Method to use when averaging periodograms. 
  Defaults to ‘mean’.

  See more detailed explanation in [scipy.signal.welch](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)

#### Return : `mcgpy.series.FrequencySeries`

* if the dataset is one-dimensional,
  return psd frequency-series
           
* if the dateset is two-dimensional,
  return psd frequency-series for each channel

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.psd(2,1)
[[16.390747, 62.977136, 149.35229, …, 1.8138222, 1.4555211, 0.93069027], 
 [582.88645, 12969.614, 68385.748, …, 3.2238317, 3.4013085, 0.5242243], 
 …, 
 [155.65072, 2010.1159, 3214.8239, …, 2.7720054, 3.6474833, 1.02261], 
 [23574.937, 160619.55, 48710.946, …, 3.823116, 3.8062277, 0.64296479]]1×10−30T2Hz
```

---
#### read(number=None, label=None, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.read(number=None, label=None, **kwargs)

Read one channel data from the dataset.

#### Parameters

* **number** : `int`, conditional

  number of a channel, while label parameter is None
    
* **label** : `str`, conditional

  label of a channel, while number parameter is None

#### Return : `mcgpy.timeseries.TimeSeries`

a single channel time-series data

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.read(number=1)
[136.26814, 156.5814, …, −67.710876, 33.009052]1×10−15T
```

---
#### rms(stride=1, **kwargs)

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.rms(stride=1, **kwargs)

Get the rms dataset by a given stride.

#### Parameters

* **stride** : `int`, `float`, `astropy.units.Quantity`, optional

  sliding step for rms calculation

#### Return : `mcgpy.timeseries.TimeSeriesArray`

* if the dataset is one-dimensional,
  return rms series
           
* if the dateset is two-dimensional,
  return rsm series for each channel

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.rms()
[[397.35058, 475.13264, 335.78015, …, 375.31408, 345.16582, 385.43835],
[667.53699, 810.86134, 459.06969, …, 595.80191, 563.2746, 617.1745], 
…, 
[1497.2229, 1485.2231, 1497.0368, …, 2169.8838, 2085.6369, 2026.235], 
[2499.4694, 2532.6463, 2630.5988, …, 2015.9665, 666.48291, 1291.5833]]1×10−15T
```

---
#### to_avg()

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.to_abg()

Calculate an average of channel signals.

#### Raises

* **TypeError**

  if the dataset was one-dimensional

#### Return : `mcgpy.timeseries.TimeSeriesArray`

an average of channel signals, 1D-array

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.to_avg()
[−308.02403, −316.00424, …, −549.95943, −541.59633]1×10−15T
```

---
#### to_rms()

_def_ **mcgpy.timeseriesarray.TimeSeriesArray**.to_rms()

Calculate the rms for all channels.

#### Raises

* **TypeError**

  if the dataset was one-dimensional

#### Return : `mcgpy.timeseries.TimeSeriesArray`

rms time-series, 1D-array

#### Examples

```python
>>> from mcgpy.timeseries import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> dataset.to_rms()
[1881.8758, 1874.3042, …, 1929.9437, 1915.6712]1×10−15T
```
