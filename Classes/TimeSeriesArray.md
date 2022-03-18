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
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.biosemi)
'MCGpy schoool'
```

---
#### channels 

Channel information table of numbers and labels

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
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
>>> from mcgpy.timeseriesarray import TimeSeriesArray
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
>>> from mcgpy.timeseriesarray import TimeSeriesArray
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
>>> from mcgpy.timeseriesarray import TimeSeriesArray
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
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.duration)
<Quantity 10. s>
```
---
#### label

Label of a channel magnetic field if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
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
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.labels)
array(['label_1', 'label_2', 'label_3', 'label_4', 'label_5', 'label_6', 'label_7', 'label_8'], dtype='<U3')
```
#### note

It might be included with the patient information or medical options.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
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
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> ch1 = dateset.read(number=1)
>>> print(ch1.number)
1

```
#### numbers

Numbers of channel magnetic fields if `mcgpy.timeseriesarray.TimeSeriesArray` is two-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.numbers)
array([ 1,  2,  3,  4,  5,  6,  7,  8])
```
---
### position

The sensor direction for measuring a magnetic field if `mcgpy.timeseriesarray.TimeSeriesArray` is one-dimentaional.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
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
>>> from mcgpy.timeseriesarray import TimeSeriesArray
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
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.sampe_rate)
<Quantity 1024 Hz>
```
---
#### t0

The first data point of time-axis.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.t0)
<Quantity 2082875272. s>
```
---
#### times

The time-axis coordinate.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.times)
<Quantity [1.08287527e+09, 1.08287527e+09, ...,1.08287528e+09] s>
```
---
#### unit

The physical unit of the data.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> dataset = TimeSeriesArray('~/test/data/file.hdf5')
>>> print(dataset.unit)
Unit("1e-15 T")
```
---


## Methods Documentation

#### area(start, end, **kwargs)
bla bla

---
#### asd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)
bla bla

---
#### at(epoch, **kwargs)
bla bla

---
#### bandpass(lfreq, hfreq, order=4, **kwargs)
bla bla

---
#### crop(start, end, **kwargs)
bla bla

---
#### exclude(numbers=None, labels=None, **kwargs)
bla bla

---
#### fft()
bla bla

---
#### highpass(hfreq, order=2, **kwargs)
bla bla

---
#### integral(start, end, **kwargs)
bla bla

---
#### lowpass(lfreq, order=2, **kwargs)
bla bla

---
#### notch(freq, Q=30, **kwargs)
bla bla

---
#### offset_correction(interval=2, **kwargs)
bla bla

---
#### offset_correction_at(epoch, **kwargs)
bla bla

---
#### psd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)
bla bla

---
#### read(number=None, label=None, **kwargs)
bla bla

---
#### rms(stride=1, **kwargs)
bla bla

---
#### to_avg()
bla bla

---
#### to_rms()
bla bla
