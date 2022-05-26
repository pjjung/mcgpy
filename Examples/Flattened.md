---
sort: 1
---

# Signal baseline correction

bla bla

```python
>>> from mcgpy.timeseries import TimeSeries
>>> data = TimeSeries('~/test/raw/file/path.hdf5', number=1)
```

```python
>>> import matplotlib.pyplot as plt
>>> fig, ax = plt.subplots(figsize=(18, 6))
>>> ax.plot(data)
>>> plt.grid(True)
>>> plt.show()
```

[(plot)](https://github.com/pjjung/mcgpy/blob/gh-pages/imgs/example-flattened-1.png)

![example-flattened-1](../imgs/example-flattened-1.png)

## Asymmetric Least Squares (ALS) method

bla bla

```sh
>>> data_flattened = data.flattened()
>>> fig, ax = plt.subplots(figsize=(18, 6))
>>> ax.plot(data_flattened)
>>> plt.grid(True)
>>> plt.show()
```
[(plot)](https://github.com/pjjung/mcgpy/blob/gh-pages/imgs/example-flattened-2.png)

![example-flattened-1](../imgs/example-flattened-2.png)

## References

* [`mcgpy.timeseriesarray.TimeSeries`](https://pjjung.github.io/mcgpy/Classes/TimeSeries.html)
* [`mcgpy.timeseriesarray.TimeSeriesArray`](https://pjjung.github.io/mcgpy/Classes/TimeSeriesArray.html)
* [Shixuan He, et atl., Analytical Methods, 6 (12), 4402, 2014](https://doi.org/10.1039/C4AY00068D)
