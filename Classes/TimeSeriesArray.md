---
sort: 2
---

# TimeSeriesArray

*class* **mcgpy.timeseriesarray.TimeSeriesArray**(source, config=None, positions=None, directions=None, unit=None, t0=None, sample_rate=None, times=None, **kwargs)

bla bla

## Parameters

* source
* config
* positions
* directions
* unit
* t0
* sample_rate
* times

```note
bla bla
```

## Properties Summary

| Properties     | Discription |
|----------------|-------------|
| [biosemo](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#biosemi)      | Bar         |
| [channels](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#channels)      | Bar         |
| [datetime](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#datetime)    | Bar         |
| [direction](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#direction)  | Bar         |
| [directions](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#directions)  | Bar         |
| [duration](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#duration)    | Bar         |
| [label](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#label)          | Bar         |
| [labels](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#labels)          | Bar         |
| [note](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#note)            | Bar         |
| [number](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#number)        | Bar         |
| [numbers](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#numbers)        | Bar         |
| [position](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#position)    | Bar         |
| [positions](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#positions)    | Bar         |
| [sample_rate](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html#sample_rate)| Bar         |

## Methods Summary

| Methods        | Discription |
|----------------|-------------|
| [area()]()           |             |
| [asd()]()           |             |
| [at()]()           |             |
| [bandpass()]()           |             |
| [crop()]()           |             |
| [exclude()]()           |             |
| [fft()]()           |             |
| [highpass()]()           |             |
| [integral()]()           |             |
| [lowpass()]()           |             |
| [notch()]()           |             |
| [offset_correction()]()           |             |
| [offset_correction_at()]()           |             |
| [psd()]()           |             |
| [read()]()           |             |
| [rms()]()           |             |
| [to_avg()]()           |             |
| [to_rms()]()           |             |


## Properties Documentation

#### biosemi
bla bla

---
#### datetime 
bla bla

---
#### direction
bla bla

---
#### duration 
bla bla

---
#### label
bla bla

---
#### note
bla bla

---
#### number
bla bla

---
### position
bla bla

---
#### sample_rate
bla bla

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

#### bandpass(lfreq, hfreq, order=4, **kwargs)
bla bla

---
#### crop(start, end, **kwargs)
bla bla

---
#### exclude(numbers=None, labels=None, **kwargs)
bla bla

#### fft()
bla bla

---
#### highpass(hfreq, order=2, **kwargs)
bla bla

---
#### integral(start, end, **kwargs)
bla bla

#### lowpass(lfreq, order=2, **kwargs)
bla bla

---
#### notch(freq, Q=30, **kwargs)
bla bla

---
#### offset_correction(interval=2, **kwargs)
bla bla

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
