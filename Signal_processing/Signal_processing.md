---
sort: 1
---

# Signal Processing

bla bla

Dependency modules are:

| Methods                 | Description                   |
|-------------------------|-------------------------------|
| [scipy.signal.butter]() |   | 
| [scipy.signal.lfilter]() |   | 
| [scipy.signal.welch]() |   | 
| [numpy.fft]() |   | 

## Time-domain filters

bla bla

It is based on `scipy`

| Methods                 | Description                   |
|-------------------------|-------------------------------|
| bandpass(lfreq, hfreq)  |   | 
| lowpass(freq)           |   |
| highpass(freq)          |   |
| notch(freq)             |   |
| rms(stride)             |   |

Here is a simple example of applying time-domain filters for single-channel data.

```python
>>> from mcgpy.timeseries import TimeSeries
>>> hdf_path = '~/test/raw/file.hdf5'
>>> data = TimeSeries(hdf_path).read(number=1)
>>> filtered_date = data.notch(60).notch(120).bandpass(1,400).lowpass(300).highpass(10).rms(1)
```

## Frequency-domain filters

bla bla

It is based on `scipy` and `numpy`

| Methods                 | Description                   |
|-------------------------|-------------------------------|
| fft()                   |   | 
| psd(seglength, overlap) |   |
| asd(seglength, overlap) |   |

Here is a simple example of applying frequency-domain filters for single-channel data.

```python
>>> from mcgpy.timeseries import TimeSeries
>>> hdf_path = '~/test/raw/file.hdf5'
>>> data = TimeSeries(hdf_path).read(number=1)
>>> fft = data.fft()
>>> asd = data.asd(2,1)
>>> psd = data.psd(2,1)
```

## Accosicated classes

Note that in addition to the TimeSeires associated classes listed below.

| Classes             | Description                   |
|---------------------|-------------------------------|
| [TimeSeriesArray]() | Dealing with a multi-channel time-series array of a MCG dataset | 
| [TimeSeires]()      | Dealing with a single time-series of a MCG dataset |
