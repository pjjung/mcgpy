---
sort: 1
---

# Timestamp

Timestamp is the stacking time as the absolute number of seconds from the epoch. This kind of counting method does not change no matter where you are located on the globe. Therefore, All time-information stored in `TimeSeires` and `TimeSeriesArray` objects are dealt with as the timestamp.

MCGpy timestamp is a way to follow time since the start of the epoch at midnight on January 1st, 1970, which is [the standard Unix timestamp](https://www.unixtimestamp.com/). And, the additional timestamp option is provided, in which [LabVIEW](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjwmKrApsz2AhXKdN4KHRotCrAQFnoECAsQAQ&url=https%3A%2F%2Fwww.ni.com%2Fen-ca%2Fsupport%2Fdocumentation%2Fsupplemental%2F08%2Flabview-timestamp-overview.html&usg=AOvVaw0zSvMA_mZguOefa6hCpKnN) records the seconds from midnight on January 1st, 1904.

For example,
| Datetime            | timestamp | type        |
|---------------------|-----------|-------------|
| 2022-02-22 02:02:02 |           | Python(Unix)|
| 2022-02-22 02:02:02 |           | Labview     |

## The time

```python
from mcgpy.time import (tconvert, to_datetime, to_timestamp)
```
bla bla

### tconvert()

```python
>>> from mcgpy.time import tconvert
>>>
```
bla bla

### to_datetime()

```python
>>> from mcgpy.time import to_datetime
>>>
```
bla bla

### to_timestamp()

```python
>>> from mcgpy.time import to_timestamp
>>>
```
bla bla

## Accosicated methods

Note that in addition to the TimeSeires associated classes listed below.

| Methods             | Description                   |
|---------------------|-------------------------------|
| [tconvert]()        |  | 
| [to_datetime]()     |  | 
| [to_timestamp]()    |  | 
