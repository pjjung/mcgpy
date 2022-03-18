---
sort: 3
---

# FrequencySeries

*class* **mcgpy.series.FrequencySeries**(data, unit=None, f0=None, df=None, frequencies=None, **kwargs)

Build time-frequency dataset.

## Parameters

* **data** : `list`, `np.ndarray`, `astropy.units.Quantity`

  frequnecy data set

* **unit** : `astropy.units.Quantity`, optional

  unit of frequency series,
  if given value is None, it will be set to time-series default unit

* **f0** : `astropy.units.Quantity`, optional

  start point of frequencies,
  if given value is None, it will be set to 0 Hz

* **df** : `astropy.units.Quantity`, optional

  interval between frequencies,
  if given valeu is None, it will be set to 1 Hz

* **frequencies** : `astropy.units.Quantity`, optional

  x-index of time-frequency series
  if given value is None, it will be built based on f0 and df

## Return : `mcgpy.series.FrequencySeries`

time-frequency array

## Examples

```python
>>> from mcgpy.series import FrequencySeries
>>> import numpy as np
>>> data = np.random.random(100)
>>> FrequencySeries(data, f0=0, df=2)
[0.14420227, 0.91460911, ..., 0.16844983, 0.54762219] 1×10−15T
>>> FrequencySeries(data, f0=0, df=2).frequencies
[0, 2, ..., 194, 196, 198] Hz
```

## Properties Summary

| Properties     | Discription |
|----------------|-------------|
| [df](https://pjjung.github.io/mcgpy/Classes/FrequencySeries.html#df)         | The inderval bwteen freqency points of freqency-axis         |
| [f0](https://pjjung.github.io/mcgpy/Classes/FrequencySeries.html#f0)         | The first data point of freqency-axis         |
| [freqencies](https://pjjung.github.io/mcgpy/Classes/FrequencySeries.html#freqencies) | The freqency-axis coordinate         |

## Methods Summary

| Methods        | Discription |
|----------------|-------------|
| [argmax()](https://pjjung.github.io/mcgpy/Classes/FrequencySeries.html#argmax)    |   Get a frequency of a maximum value in a frequency series          |
| [argmin()](https://pjjung.github.io/mcgpy/Classes/FrequencySeries.html#argmin)    |   Get a frequency of a minimum value in a frequency series          |
| [at(freq)](https://pjjung.github.io/mcgpy/Classes/FrequencySeries.html#atfreq)    |   Get a value at an input frequnecy          |
| [crop(start, end)](https://pjjung.github.io/mcgpy/Classes/FrequencySeries.html#cropstart-end)    |  Crop a series within an input range   |

## Properties Documentation

#### df

he inderval bwteen freqency points of freqency-axis.

Here is an example:

```python
>>> from mcgpy.series import FrequencySeries
>>> import numpy as np
>>> source = np.ranmdom.random(100)
>>> fs = FrequencySeries(source, f0=0, df=2)
>>> print(fs.df)
<Quantity 2 Hz>
```
---
#### f0

The first data point of freqency-axis.

Here is an example:

```python
>>> from mcgpy.series import FrequencySeries
>>> import numpy as np
>>> source = np.ranmdom.random(100)
>>> fs = FrequencySeries(source, f0=0, df=2)
>>> print(fs.f0)
<Quantity 0 Hz>
```
---
#### freqencies

The freqency-axis coordinate.

Here is an example:

```python
>>> from mcgpy.series import FrequencySeries
>>> import numpy as np
>>> source = np.ranmdom.random(100)
>>> fs = FrequencySeries(source, f0=0, df=2)
>>> print(fs.freqencies)
<Quantity [0., 2., ..., 46, 48] Hz>
```
---


## Methods Documentation

#### argmax()

_def_ **mcgpy.series.FrequencySeries**.argmax()

Get a frequency of a maximum value in a frequency series.

#### Return : `astropy.units.Quantity`

a frequency of the maximum value

#### Examples

```python
>>> from mcgpy.series import FrequencySeries
>>> import numpy as np
>>> source = np.ranmdom.random(100)
>>> fs = FrequencySeries(source, f0=0, df=2)
>>> fs.argmax()
54 Hz
```

---
#### argmin()

_def_ **mcgpy.series.FrequencySeries**.argmin()

Get a frequency of a minimum value in a frequency series.

#### Return : `astropy.units.Quantity`

a frequency of the minimum value

#### Examples

```python
>>> from mcgpy.series import FrequencySeries
>>> import numpy as np
>>> source = np.ranmdom.random(100)
>>> fs = FrequencySeries(source, f0=0, df=2)
>>> fs.argmin()
20 Hz
```
---
#### at(freq)

_def_ **mcgpy.series.FrequencySeries**.at(freq)

Get a value at an input frequnecy.

### Parameters

* **freq** : `int`, `float`, `astropy.units.Quantity`

  a frequency user want to get the value

#### Return : `astropy.units.Quantity`

the value at an input frequency

#### Examples

```python
>>> from mcgpy.series import FrequencySeries
>>> import numpy as np
>>> source = np.ranmdom.random(100)
>>> fs = FrequencySeries(source, f0=0, df=2)
>>> fs.at(30)
0.74917808 1×10−15T
```
---
#### crop(start, end)

_def_ **mcgpy.series.FrequencySeries**.crop(start, end)

Crop a series within an input range.

### Parameters

* **start** : `int`, `float`, `astropy.units.Quantity`
    
* **end** : `int`, `float`, `astropy.units.Quantity`
    
#### Return : `mcgpy.series.FrequencySeries`

cropped frequency series

#### Examples

```python
>>> from mcgpy.series import FrequencySeries
>>> import numpy as np
>>> source = np.ranmdom.random(100)
>>> fs = FrequencySeries(source, f0=0, df=2)
>>> fs.crop(20,50)
[0.74373018, 0.073202608, ..., 0.53898833, 0.62487978] 1×10−15T
```
---
