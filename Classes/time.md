---
sort: 5
---

# time

```python
from mcgpy.time import (tconvert, to_timestamp, to_datetime)
```

## Functions sumarry

| Functions | Description |
|-----------|-------------|
| [tconvert(timeinput, ttype)](https://pjjung.github.io/mcgpy/Classes/time.html#the-timetconvert) | Convert the timestamp (Unix or LabVIEW  type) to the datetime string, vice versa |
| [to_timestamp(timeinput, ttype)](https://pjjung.github.io/mcgpy/Classes/time.html#the-timeto_timestamp) | Convert the datetime string to the timestamp (Unix or LabVIEW  type) |
| [to_datetime(timeinput, ttype)](https://pjjung.github.io/mcgpy/Classes/time.html#the-timeto_datetime) | Convert the the timestamp (Unix or LabVIEW  type) to the datetime string |

## The time.tconvert

*def* **mcgpy.time.tconvert**(timeinput, ttype='python')

time converter

### Parameters

* **timeinput** :  `str`, `int`, `float`
 
  input value takes timestamp, datetime, or special string

* **ttype** : {"python", "labview"}, optional

  the standard of timestamp, default value is "python"
 
  - in case of "python", timestamp will be calculated from "1970-01-01 09:00:00.000000"
  
  - in case of "labveiw", timestamp will be calculated from "1904-01-01 00:00:00.000000"

### Raises

* **ValueError**

  input datetime format is no `%Y-%m-%d %H:%M:%S.%f`
    
### Return

  - if input is timestamp,
  return the datetime : `str`
  - if input is datatime,
  return timestamp : `float`
  - if input is special string; "now", "today", "tomorrow", or "yesterday",
  return related timestamp : `float`

### Examples

```python
>>> from mcgpy.time import tconvert
>>> tconvert(0)
"1970-01-01 09:00:00.000000"
>>> tconvert(0, ttype="labview")
"1904-01-01 00:00:00.000000"
>>> tconvert("1970-01-01 09:00:00.000000", ttype="labview")
2082875272.0
```

---

## The time.to_timestamp

*def* **mcgpy.time.to_timestamp**(timeinput, ttype='python', *args, **kwargs)

converto datetime to timestamp

### Parameters

* **timeinput** : `str`

  input value takes "%Y-%m-%d %H:%M:%S.%f" style datetime string,


* **ttype** : {"python", "labview"}, optional

  the standard of timestamp, default value is "python"
  
  * in case of "python", timestamp will be calculated from "1970-01-01 09:00:00.000000"
  
  * in case of "labveiw", timestamp will be calculated from "1904-01-01 00:00:00.000000"

### Raises

* **ValueError**

  input datetime format is no `%Y-%m-%d %H:%M:%S.%f`

### Return : `float`

  * timestamp
  * if `int` or `float` value is inserted, return input value

### Examples

```python
>>> from mcgpy.time import to_timestamp
>>> to_timestamp("2000-01-01 00:00:00")
946652400.0
```

---

## The time.to_datetime

*def* **mcgpy.time.to_datetime**(timeinput, ttype='python', *args, **kwargs)

convert from timestamp to datetime

### Parameters

* **timeinput** : `int`, `float`

  the value of timestamp

* **ttype** :{"python", "labview"}, optional

  the standard of timestamp, default value is "python"
  
  * in case of "python", timestamp will be calculated from "1970-01-01 09:00:00.000000"
 
  * in case of "labveiw", timestamp will be calculated from "1904-01-01 00:00:00.000000"

### Return : `str`

  datetime string as `%Y-%m-%d %H:%M:%S.%f`

### Examples

```python
>>> from mcgpy.time import to_datetime
>>> to_timestamp(0)
1970-01-01 09:00:00.000000
```
