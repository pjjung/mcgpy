---
sort: 4
---

# FieldMap

*class* **mcgpy.numeric.FieldMap**(data,
              sourcegrid_width=240, sourcegrid_height=-40, sourcegrid_interval=16,
              sensorgrid_width=400, sensorgrid_height=40, sensorgrid_interval=25,
              baseline=50, axis='z', conduct_model='horizontal', eigenvalues=10, **kwargs)

Calculate magnetic field maps on the sersor plane.

## Parameters

* **data** : `mcgpy.timeseriesarra.TimeSeriesArray`

  MCG dataset 1) at the certain time point
              2) between certain duration

* **sourcegrid_width** : `int`, `float`, `astropy.units.Quantity`, optional

  width of source grid, default value is 240 [mm], but it depends on device properties

* **sourcegrid_height** : `int`, `float`, `astropy.units.Quantity`, optional

  height of source grid, default value os -40 [mm], but it depends on device properties

* **sourcegrid_interval** : `int`, `float`, `astropy.units.Quantity`, optional

  interval of cells on source grid, default value is 16 [mm], but it depends on device properties

* **sensorgrid_width** : `int`, `float`, `astropy.units.Quantity`, optional

  width of sensor grid, default value is 400 [mm], but it depends on device properties

* **sensorgrid_height** : `int`, `float`, `astropy.units.Quantity`, optional

  height of sensor grid, defualt value is 40 [mm], but it depends on device properties

* **sensorgrid_interval** : `int`, `float`, `astropy.units.Quantity`, optional

  interval of cells on sensor grid, default value is 25 [mm], but it depends on device properties

* **baseline** : `int`, `float`, `astropy.units.Quantity`, optional

  length of baseline (Z-axis length of sensor), defualt value is 50 [mm], but it depends on device properties

* **axis** : `{x, y, z}`, optional

  axis of magnetic vectors on sensor grid, default value is z

* **conduct_model** : `{spherical, horizontal, free}`, optional

  conduct model about sources, default value is horizontal

* **eigenvalues** : `int`, optional

  the number of eigenvalues to get quasi-inverser lead field matrix, default value is 10

```warning
Grid related parameters and sensor's baseline depend on device properties. If they did not match the instrument obtained MCG signals, it is possible to get inaccuracy results.
```

## Raises

* **TypeError**

  if input data type is not `mcgpy.timeseriesarray.TimeSeriesArray`

## Return : `mcgpy.numerical.FieldMap`

* if the dimension of input dataset is one
  2D-array, amplitude of given direction of magnetic vector on sensor plane

* if the dimension of input dataset is two
   3D-array, amplitude of given direction of magnetic vectors on sensor plane

## Examples

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
>>> epoch_dataset = dataset.at(1126259462)
>>> LeadField(epoch_dataset)
[[−1.2890067, −1.4466162, −1.6401107, …, 0.17438883, 0.30280878, 0.38030763], [−1.4262029, −1.6297339, −1.9009002, …, 0.4317918, 0.53622291, 0.58182473], 
[−1.5804608, −1.8479563, −2.234106, …, 0.84135491, 0.86858131, 0.84406456], …, [−0.76191537, −0.75202421, −0.66326362, …, 2.2549908, 1.8901924, 1.6201124]]1×10−15T
>>>
>>> duration_dataset =  dataset.crop(1126259462, 1126259470)
>>> LeadField(epoch_dataset)
[[[−1.2890067, −1.4466162, −1.6401107, …, 0.17438883, 0.30280878, 0.38030763], ..., [−1.4262029, −1.6297339, −1.9009002, …, 0.4317918, 0.53622291, 0.58182473]], 
...
[[−1.5804608, −1.8479563, −2.234106, …, 0.84135491, 0.86858131, 0.84406456], ..., [−0.76191537, −0.75202421, −0.66326362, …, 2.2549908, 1.8901924, 1.6201124]]]1×10−15T
```

## Properties Summary

| Properties     | Discription |
|----------------|-------------|
| [X](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#x)      | X-axis meshgrid         |
| [Y](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#y)      | Y-axis mechgrid         |
| [datetime](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#datetime)      | The data time at the point of data recording i.e., ‘2020-02-02 02:02:02.00000'         |
| [dt](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#dt)      | The inderval bwteen time points of time-axis         |
| [duration](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#duration)      | Data recording duration         |
| [sample_rate](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#sample_rate)      | Data sample frequency  |
| [t0](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#t0)      | The first data point of time-axis         |
| [times](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#times)      | The time-axis coordinate         |

```note
Properties of the `mcgpy.numeric.FieldMap` class only provide reading metadata to prevent incorrect value use.
```

```note
`dt`, `diration`, `sample_rate`, and `times` are `None` if the input dataset is one-diemtional. This is because Field Map is calculated by magnetic field values at the epoch.
```

## Methods Summary

| Methods        | Discription |
|----------------|-------------|
| [arrows()](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#arrows)      | Calculate current vectors on the sensor plane and make table         |
| [pole()](https://pjjung.github.io/mcgpy/Classes/FieldMap.html#pole)      | Calculate a field current vector on the sensor plane and make table         |

## Properties Documentation

#### X

X-axis meshgrid.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
>>> Bz = LeadField(dataset)
>>> print(Bz.X)
<Quantity [[−200, −175, −150, …, 150, 175, 200], [−200, −175, −150, …, 150, 175, 200], [−200, −175, −150, …, 150, 175, 200], …, [−200, −175, −150, …, 150, 175, 200], [−200, −175, −150, …, 150, 175, 200], [−200, −175, −150, …, 150, 175, 200]]mm >
```

---
#### Y

Y-axis mechgrid.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
>>> Bz = LeadField(dataset)
>>> print(Bz.Y)
<Quantity [[−200, −200, −200, …, −200, −200, −200], [−175, −175, −175, …, −175, −175, −175], [−150, −150, −150, …, −150, −150, −150], …, [150, 150, 150, …, 150, 150, 150], [175, 175, 175, …, 175, 175, 175], [200, 200, 200, …, 200, 200, 200]]mm >
```

---
#### datetime

The data time at the point of data recording i.e., ‘2020-02-02 02:02:02.00000'.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5").crop(1643734922, 1643734930)
>>> Bz = LeadField(dataset)
>>> print(Bz.datetime)
'2022-02-02 02:02:02'
```

---
#### dt

The inderval bwteen time points of time-axis.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5").crop(1643734922, 1643734930)
>>> Bz = LeadField(dataset)
>>> print(Bz.dt)
<Quantity 0.0009765625 s >
```

---
#### duration

Data recording duration.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5").crop(1643734922, 1643734930)
>>> Bz = LeadField(dataset)
>>> print(Bz.duration)
<Quantity 8 s>

```

---
#### sample_rate

Data sample frequency.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5").crop(1643734922, 1643734930)
>>> Bz = LeadField(dataset)
>>> print(Bz.sample_rate)
<Quantity 1024. Hz>
```

---
#### t0

The first data point of time-axis.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5").crop(1643734922, 1643734930)
>>> Bz = LeadField(dataset)
>>> print(Bz.t0)
<Quantity 1.64373492e+09 s>
```

---
#### times

The time-axis coordinate.

Here is an example:

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5").crop(1643734922, 1643734930)
>>> Bz = LeadField(dataset)
>>> print(Bz.times)
<Quantity [1.64373492e+09, 1.64373492e+09, 1.64373492e+09, ...,1.64373492e+09, 1.64373492e+09] s>
```

---

## Methods Documentation

#### arrows()

*def* **mcgpy.numeric.FieldMap**.arrows()

Calculate current vectors on the sensor plane and make table.

##### Return 

* if the dimension of input dataset is one : `astropy.table.QTable`

  table contains current arrows on sensor plane: tail coordinate, head coordinate, vector, and distance
        
* if the dimension of input dataset is two : `astropy.table.QTable`

  dictionanty consists of a table at each time
    
##### Examples

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
>>> epoch_dataset = dataset.at(1643734922)
>>> LeadField(epoch_dataset).arrows()
tails 	              heads	                 vectors	    distances
float64	              float64	             complex128	    float64
(-200.0,0.0,-200.0)	  (-200.13,0.0,-200.15)	(-0.13-0.15j) 	0.20
(-175.0,0.0,-200.0)	  (-175.18,0.0,-200.17)	(-0.18-0.17j)  	0.25
.
.
.
>>> duration_dataset =  dataset.crop(1643734922, 1643734930)
>>> LeadField(epoch_dataset)
{1126259462:
tails 	              heads	                 vectors	    distances
float64	              float64	             complex128	    float64
(-200.0,0.0,-200.0)	  (-200.13,0.0,-200.15)	(-0.13-0.15j) 	0.20
(-175.0,0.0,-200.0)	  (-175.18,0.0,-200.17)	(-0.18-0.17j)  	0.25
.
.
.
,...}
```

---
#### pole()

*def* **mcgpy.numeric.FieldMap**.pole()

Calculate a field current vector on the sensor plane and make table.

##### Return 

* if the dimension of input dataset is one : `astropy.table.QTable`

  table contains a field current arrow on sensor plane: minimum coordinates, maximum coordinate, vector, distance, anngle, and ratio
        
* if the dimension of input dataset is two : `astropy.table.QTable`

  table contains ontains a field current arrows on sensor plane during at each time: minimum coordinates, maximum coordinate, vector, distance, anngle, and ratio
    
##### Examples

```python
>>> from mcgpy.timeseriesarray import TimeSeriesArray
>>> from mcgpy.numeric import LeadField
>>> dataset = TimeSeriesArray("~/test/raw/file/path.hdf5")
>>> epoch_dataset = dataset.at(1643734922)
>>> LeadField(epoch_dataset).pole()
type         	1643734922 s
str14        	object
min coordinate	(-75.0, -100.0)
max coordinate	(75.0, 100.0)
vector	        (150+0j)
distance	    150.0
angle	        -0.0 deg
ratio	        0.76948964274897
>>>
>>> duration_dataset =  dataset.crop(1643734922, 1643734930)
>>> LeadField(epoch_dataset)
type         	1643734922 s         	1643734922.29296875 s         	...
str14        	object         	        object                      	...
min coordinate	(-75.0, -100.0)         (-75.0, -100.0)             	...
max coordinate	(75.0, 100.0)           (75.0, 100.0)               	...
vector	        (150+0j)                (150+0j)         	            ...
distance	    150.0                   150.0         	                ...
angle	        -0.0 deg                -0.0 deg         	            ...
ratio	        0.76948964274897        0.76948964274897              	...
'''
```

---