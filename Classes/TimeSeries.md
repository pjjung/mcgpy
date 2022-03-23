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
| [argmax()]() | Find the epoch of the maximum value |
| [argmin()]() | Find the epoch of the minimum value |
| [asd(fftlength, overlap, window, average)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#asdfftlengthnone-overlap0-windowhann-averagemedian-kwargs)      |   Calculate the acceleration spectral density, ASD     |
| [at(epoch)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#atepoch-kwargs)       | Peak up the value at an input time           |
| [bandpass(lfre, hfreq, order)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#bandpasslfre-hfreq-order4-kwargs) | Apply the bandpass filter to the data         |
| [crop(start, end)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#cropstart-end-kwargs)     | Slice the time-series between start and end times         |
| [fft()](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#fft)      | Calculate the fast Fourier transform, FFT         |
| [flattened(freq)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#flattenedfreq1-kwargs) | Flatten a wave-form by a lowpass filter |
| [highpass(hfreq, order)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#highpasshfreq-order2-kwargs) | Apply the highpass filter to the data         |
| [lowpass(lfreq, order)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#lowpasslfreq-order2-kwargs)  | Apply the lowpass filter to the data         |
| [max()]() | Find the maximum value |
| [min()]() | Find the minimum value |
| [notch(freq, Q)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#notchfreq-q30-kwargs)    | Apply the notch/bandstop filter to the data         |
| [psd(fftlength, overlap, window, average)](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#psdfftlengthnone-overlap0-windowhann-averagemedian-kwargs)      | Calculate the power spectral density, PSD         |
| [rms(rms(stride))](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html#rmsstride1-kwargs)      | Get the rms series by a given stride       |

## Properties Documentation

#### biosemi

Identification code _i.e., National Hospital, National Reaserch, …_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.biosemi)
'MCGpy school'
```

---
#### datetime 

The data time at the point of data recording _i.e., ‘2020-02-02 02:02:02.00000'_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.datetime)
'2020-02-02 02:02:02'
```

---
#### direction

The sensor direction for measuring a magnetic field _i.e., [1.,0.,0.]_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.direiction)
array([1, 0, 0])
```

---
#### dt 

The inderval bwteen time points of time-axis, default value is $$1 s$$ if the input data had no metadata.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.dt)
<Quantity 1. s>
```

---
#### duration 

Here is an example:

Data recording duration

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.duration)
<Quantity 8. s>
```

---
#### label

Label of a channel _i.e., X1, Y1, Z1, …_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.label)
'label_1'
```

---
#### note

It might be included with the patient information or medical options.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
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
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.number)
1
```

---
### position

The sensor coordinate on the sensor grid _i.e., [0., 0., 0.,]_

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.position)
array([0, 0, 0])
```

---
#### sample_rate

Data sample frequency, default value is $$1 Hz$$ if the input data had no metadata.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.sample_rate)
<Quantity 1 Hz>
```

---
#### t0

The first data point of time-axis, default value is $$0 s$$ if the input data had no metadata.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.t0)
<Quantity 0. s>
```

---
#### times

The time-axis coordinate.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.times)
<Quantity [0, 1, 2 ..., 8] s>
```

---
#### unit

The physical unit of the data, default unit is $$1 fT$$ if the input data had no metadata.

Here is an example:

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/data/file.hdf5', number=1)
>>> print(data.unit)
Unit("1e-15 T")
```

---

## Methods Documentation

#### argmax()

_def_ **mcgpy.timeseries.TimeSeries**.argmax()

Find the epoch of the maximum value 

##### Return : `astropy.table.Quantity`

a timestamp of the maximum value

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.max()
4480.30971×10−15T
>>> data.argmax()
11.3447265625 s
```
---
#### argmin()

_def_ **mcgpy.timeseries.TimeSeries**.argmin()

Find the epoch of the minimum value 

##### Return : `astropy.table.Quantity`

a timestamp of the minimum value

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.min()
53.7786021×10−15T
>>> data.argmin()
10 s
```
---
#### asd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)

_def_ **mcgpy.timeseries.TimeSeries**.asd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)

Calculate the acceleration spectral density, ASD

##### Parameters

* **seglength** : `int`,  `float`, optional

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
  
  See more detailed explanation in "scipy.signal.welch"

* **average** : { "mean", "median" }, optional

  Method to use when averaging periodograms. 
  Defaults to ‘mean’.

  See more detailed explanation in [scipy.signal.welch](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html)

##### Return : `mcgpy.series.FrequencySeries`

asd frequency-series

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.asd(2,1)
[16.390747, 62.977136, 149.35229, …, 1.8138222, 1.4555211, 0.93069027]1×10−15THz1/2
```

---
#### at(epoch, **kwargs)

_def_ **mcgpy.timeseries.TimeSeries**.at(epoch, **kwargs)

Peak up the value at an input time

##### Parameters

* **epoch** : `int`, `float`, `astropy.units.Quantity`

  timestamp user wants to get the value

#### Return : `mcgpy.timeseries.TimeSeries`

the valeu at an input timestamp

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.at(8)
136.268141×10−15T
```

---
#### bandpass(lfre, hfreq, order=4, **kwargs) 

_def_ **mcgpy.timeseries.TimeSeries**.bandpass(lfreq, hfreq, order=4, flattening=True, **kwargs)

Apply the bandpass filter to the data

##### Parameters

* **lfreq** : "int", "float", "astropy.units.Quantity"

  the low cutoff frequencies 
        
* **hfreq** : "int", "float", "astropy.units.Quantity"

  the high cutoff frequencies 
  
* **sample_rate** : "int", "float", "astropy.units.Quantity"

  sample rate of ditital signal
  
* **order** : "int", optional

  the order of the filter, default value is 4

* **flattening** : `Boonlean`, optional

  signal flattening option, defaule value is True

##### Return : `mcgpy.timeseries.TimeSeries`

filted series

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.bandpass(0.1, 200)
[5.8798634, 35.303578, …, 27.332395, 18.921922]1×10−15T
```

---
#### crop(start, end, **kwargs)

_def_ **mcgpy.timeseries.TimeSeries**.crop(start, end, **kwargs)

Slice the time-series between start and end times.

##### Parameters

* **start** : `int`, `float`, `astropy.units.Quantity`

  start timestamp
    
* **end** : `int`, `float`, `astropy.units.Quantity`

  end timestamp

##### Return : `mcgpy.timeseries.TimeSeries`

sliced time-series array

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.crop(10,12)
[136.26814, 156.5814, …, −256.45494, −223.44589]1×10−15T
```

---
#### fft()

_def_ **mcgpy.timeseries.TimeSeries**.fft()

Calculate the fast Fourier transform, FFT.

##### Return : `mcgpy.series.FrequencySeries`

fft frequency-series

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.fft()
[92.382265, 16.48454, …,  0.27365534, 0.2273498]1×10−15T
```

---
#### flattened(freq=1, **kwargs)

_def_ **mcgpy.timeseries.TimeSeries**.flattened(freq=1, **kwargs)

Flattened a wave form by a lowpass filter

##### Parameters

* **freq** : `int`, `float`, `astropy.units.Quantity`

  the frequency for the lowpass filter

##### Return : `mcgpy.timeseries.TimeSeries`

(original signal) - (lowpass filtered signal)

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.flattened(1)
 [−691.04563, −728.74299, −612.39823, …, −400.13071, −465.25414, −410.18831]1×10−15T
```

---

#### highpass(hfreq, order=2, **kwargs)

_def_ **mcgpy.timeseries.TimeSeries**.highpass(hfreq, order=2, flattening=True, **kwargs)

apply the highpass filter to the data.

##### Parameters

* **hfreq** : `int`, `float`, `astropy.units.Quantity`

  the cutoff frequencies 

* **sample_rate** : `int`, `float`, `astropy.units.Quantity`

  sample rate of ditital signal

* **order** : `int`, optional

  the order of the filter, default value is 2

* **flattening** : `Boonlean`, optional

  signal flattening option, defaule value is True

##### Return : `mcgpy.timeseries.TimeSeries`

filted series

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.highpass(1)
[135.67819, 154.72616, …, 8.7490505, 108.60693]1×10−15T
```

---
#### lowpass(lfreq, order=2, **kwargs)

_def_ **mcgpy.timeseries.TimeSeries**.lowpass(lfreq, order=2, flattening=True, **kwargs)

Apply the lowpass filter to the data

##### Parameters

* **lfreq** : `int`, `float`, `astropy.units.Quantity`

  the cutoff frequencies 

* **sample_rate** : `int`, `float`, `astropy.units.Quantity`

  sample rate of ditital signal

* **order** : `int`, optional

  the order of the filter, default value is 2

* **flattening** : `Boonlean`, optional

  signal flattening option, defaule value is True

##### Return : `mcgpy.timeseries.TimeSeries`

filted series

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.lowpass(300)
[51.327193, 145.35014,  …, −111.09751, −31.626277]1×10−15T
```

---
### max()

Find the maximum value

### min()

Find the maximum value

#### notch(freq, Q=30, **kwargs)

_def_ **mcgpy.timeseries.TimeSeries**.notch(freq, Q=30, flattening=True, **kwargs)

Aply the notch/bandstop filter to the data.

##### Parameters

* **freq** : `int`, `float`, `astropy.units.Quantity`

 the cutoff frequencies 

* **sample_rate** : `int`, `float`, `astropy.units.Quantity`

 sample rate of ditital signal

* **Q** : `int`, optional

 the Q-factor of the filter, default value is 30

* **flattening** : `Boonlean`, optional

  signal flattening option, defaule value is True

##### Return : `mcgpy.timeseries.TimeSeries`

filted series

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.notch(60)
[135.4371, 154.08522,  …, −57.510631, 44.525834]1×10−15T
```

---
#### psd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)

_def_ **mcgpy.timeseries.TimeSeries**.psd(fftlength=None, overlap=0, window='hann', average='median', **kwargs)

Calculate the power spectral density, PSD.

##### Parameters

* **fftlength** : `int`,  `float`, optional

  number of seconds for dividing the time window into equal bins,
  if None type value is given, it will be the size of signal

* **overlap** : `int`, `float`, optional
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
        
##### Return : `mcgpy.series.FrequencySeries`

psd frequency-series

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.psd(2,1)
[268.6566, 3966.1196, 22306.108, …, 3.2899511, 2.1185417, 0.86618438]1×10−30T2Hz
```

---

#### rms(stride=1, **kwargs)

_def_ **mcgpy.timeseries.TimeSeries**.rms(stride=1, **kwargs)

Get the rms series by a given stride

##### Parameters

* **stride** : `int`, `float`, `astropy.units.Quantity`, optional

  sliding step for rms calculation

##### Return : `mcgpy.timeseries.TimeSeries`

rms series

##### Examples

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries("~/test/raw/file/path.hdf5", number=1)
>>> data.rms()
[397.35058, 475.13264, ..., 345.16582, 385.43835]1×10−15T
```

---
