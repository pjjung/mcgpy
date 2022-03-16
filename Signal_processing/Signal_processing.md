---
sort: 1
---

# Signal processing

Though magnetocardiography (MCG) devices are designed to measure the magnetic signal related to the cardiac activitiy, many instrumental error signals and environmental noises are recorded at the same time. Signal processing techniques are used to emphasize or detect components we have an interest in measured datasets. MCGpy also provides common signal processing methods by [scipy.signal](https://docs.scipy.org/doc/scipy/reference/signal.html) and [numpy.fft](https://numpy.org/doc/stable/reference/routines.fft.html#module-numpy.fft) as `class methods` for convenience.

Dependency modules are:
* [scipy.signal.butter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html) - Butterworth digital and analog filter design 
* [scipy.signal.lfilter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lfilter.html) - Filter data along one-dimension with an IIR or FIR filter 
* [scipy.signal.welch](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html) - Estimate power spectral density using Welch’s method  
* [numpy.fft.fft](https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html) - Compute the one-dimensional discrete Fourier Transform 

## Time-domain filters

bla bla

It is based on `scipy`

| Methods                   | Description                   |
|---------------------------|-------------------------------|
| `bandpass(lfreq, hfreq)`  |   | 
| `lowpass(freq)`           |   |
| `highpass(freq)`          |   |
| `notch(freq)`             |   |
| `rms(stride)`             |   |

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
| `fft()`                   |   | 
| `psd(seglength, overlap)` |   |
| `asd(seglength, overlap)` |   |

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
