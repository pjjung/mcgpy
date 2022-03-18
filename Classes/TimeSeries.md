---
sort: 1
---

# TimeSeries

*class* **mcgpy.timeseries.TimeSeries**(source, number=None, label=None, unit=None, t0=None, sample_rate=None, times=None, *args, **kwargs)

Make a single-channel time-series array with metadata.

## Parameters

* **source** : `str`, `list`, `np.ndarray`, `astropy.units.Quantity`, `mcgpy.io.Array`

  it can take multi-type data formats

* **number** : `int`, conditional

  channel's number
  * if the input source is the path of a raw file and the label is None value, this parameter is essential for reading a channel data
  * if the input source is the data array, this parameter is optional

* **label** : `str`, conditional

  channel's label
  * if the input source is the path of a raw file and the number is None value, this parameter is essential for reading a channel data
  * if the input source is the data array, this parameter is optional

* **unit** : `astropy.units.Quantity`, optional

  an unit of data
  
  default unit is femto tesla, 10E-15 T, if the input source is not a raw file path

* **t0**: `int`, `float`, `astropy.units.Quantity`, optional

  start time of time-series

  default value is 0 s, if the input source is not a raw file path

* **sampel_rate** : `int`, `float`, `astropy.units.Quantity`, optional

  signal sample frequency

  default value is 1 Hz, if the input source is not a rwa file path

* **times** : `list`, `np.ndarray`, `astropy.units.Quantity`, optional

  time xindex

  default value is made by data size, t0 and sample_rate, if the input source is not a raw file path

## Return : `mcgpy.timeseries.TimeSeries`

* if the input source is the path of a raw file,
  read a data of given channel number or label, and return it. 
* if the input source is the data array,
  return the time-series array by given parameters

## Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> import numpy as np
>>> source = np.random.random(100)
>>> data = TimeSeries(source, sample_rate=10)
>>> print(data)
[0.82405757 0.34912628 ... 0.35523488 0.9324402 ] 1e-15 T
>>> print(data.times)
[0.  0.1 ... 9.8 9.9] s
>>>
>>> path = "~/test/raw/file/path.hdf5"
>>> data = TimeSeries(path, number=1)
>>> print(data)
[ 136.26813889  156.58140182  ...  -67.71087646  33.00905228] 1e-15 T
```

```note
This class is designed to deal with a single-channel time-series of MCG system, though.
User defined data array can be applied, and use its properties and methods
```

## Properties Summary

| Properties     | Discription |
|----------------|-------------|
| [biosemo](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#biosemi)      | Identification code         |
| [datetime](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#datetime)    | The data time at the point of data recording          |
| [direction](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#direction)  | The sensor direction for measuring a magnetic field          |
| [dt](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#dt)  |    The inderval bwteen time points of time-axis      | 
| [duration](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#duration)    | Data recording duration         |
| [label](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#label)          | Label of a channel          |
| [note](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#note)            | It might be included with the patient information or medical options         |
| [number](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#number)        | Number of a channel          |
| [position](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#position)    | The sensor coordinate on the sensor grid         |
| [sample_rate](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#sample_rate)| Data sample frequency         |
| [t0](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#t0)|  The first data point of time-axis      |
| [times](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#times)|  The time-axis coordinate       |
| [unit](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#unit)|   The physical unit of the data       |


## Methods Summary

| Methods        | Discription |
|----------------|-------------|
| [asd(fftlength, overlap, window, average)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#asdfftlengthnone-overlap0-windowhann-averagemedian-kwargs)      |   Calculate the acceleration spectral density, ASD     |
| [at(epoch)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#atepoch)       | Peak up the value at an input time           |
| [bandpass(lfre, hfreq, order)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#bandpasslfre-hfreq-order4) | Apply the bandpass filter to the data         |
| [crop(start, end)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#cropstart-end)     | Slice the time-series between start and end times         |
| [fft()](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#fft)      | Calculate the fast Fourier transform, FFT         |
| [highpass(hfreq, order)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#highpasshfreq-order2) | Apply the highpass filter to the data         |
| [lowpass(lfreq, order)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#lowpasslfreq-order2)  | Apply the lowpass filter to the data         |
| [notch(freq, Q)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#notchfreq-q30)    | Apply the notch/bandstop filter to the data         |
| [psd(fftlength, overlap, window, average)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#psdfftlengthnone-overlap0-windowhann-averagemedian-kwargs)      | Calculate the power spectral density, PSD         |
| [rms(rms(stride))](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#rmsstride1)      | Get the rms series by a given stride       |


## Properties Documentation

#### biosemi

Identification code _i.e., National Hospital, National Reaserch, …_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.biosemi)
'MCGpy school'
```

---
#### datetime 

The data time at the point of data recording _i.e., ‘2020-02-02 02:02:02.00000'_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.datetime)
'2020-02-02 02:02:02'
```

---
#### direction

The sensor direction for measuring a magnetic field _i.e., [1.,0.,0.]_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.direiction)
array([1, 0, 0])
```

---
#### dt 

The inderval bwteen time points of time-axis, default value is $$1 s$$ if the input data had no metadata.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.dt)
<Quantity 1. s>
```

---
#### duration 

Here is an example:

Data recording duration

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.duration)
<Quantity 8. s>
```

---
#### label

Label of a channel _i.e., X1, Y1, Z1, …_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.label)
'label_1'
```

---
#### note

It might be included with the patient information or medical options.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.note)
{'encoded info': 'a7F76ae32B2566A8F165_22221223',
 'opinion': 'Healthy',
 'patient number': '0000'}
```

---
#### number

Number of a channel _i.e., 1, 2, 3, …_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.number)
1
```

---
### position

The sensor coordinate on the sensor grid _i.e., [0., 0., 0.,]_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.position)
array([0, 0, 0])
```

---
#### sample_rate

Data sample frequency, default value is $$1 Hz$$ if the input data had no metadata.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.sample_rate)
<Quantity 1 Hz>
```

---
#### t0

The first data point of time-axis, default value is $$0 s$$ if the input data had no metadata.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.t0)
<Quantity 0. s>
```

---
#### times

The time-axis coordinate.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.times)
<Quantity [0, 1, 2 ..., 8] s>
```

---
#### unit

The physical unit of the data, default unit is $$1 fT$$ if the input data had no metadata.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5').read(number=1)
>>> print(data.unit)
Unit("1e-15 T")
```

---

## Methods Documentation

#### asd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)
bla bla

---
#### at(epoch, **kwargs)
bla bla

---
#### bandpass(lfre, hfreq, order=4, **kwargs) 
bla bla

---
#### crop(start, end, **kwargs)
bla bla

---
#### fft()
bla bla

---
#### highpass(hfreq, order=2, **kwargs)
bla bla

---
#### lowpass(lfreq, order=2, **kwargs)
bla bla

---
#### notch(freq, Q=30, **kwargs)
bla bla

---
#### psd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)
bla bla

---

#### rms(stride=1, **kwargs)
bla bla

---
