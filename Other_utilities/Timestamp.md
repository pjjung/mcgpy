---
sort: 1
---

# Timestamp

Timestamp is the stacking time as the absolute number of seconds from the epoch. This kind of counting method does not change no matter where you are located on the globe. Therefore, All time-information stored in `TimeSeires` and `TimeSeriesArray` objects are dealt with as the timestamp.

MCGpy timestamp is a way to follow time since the start of the epoch at midnight on January 1st, 1970, which is [the standard Unix timestamp](https://www.unixtimestamp.com/). And, the additional timestamp option is provided, in which [LabVIEW](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjwmKrApsz2AhXKdN4KHRotCrAQFnoECAsQAQ&url=https%3A%2F%2Fwww.ni.com%2Fen-ca%2Fsupport%2Fdocumentation%2Fsupplemental%2F08%2Flabview-timestamp-overview.html&usg=AOvVaw0zSvMA_mZguOefa6hCpKnN) records the seconds from midnight on January 1st, 1904.

For example,

| type        | Datetime            | timestamp    |
|-------------|---------------------|--------------|
| Python(Unix)| 2022-02-22 02:02:02 | 1645462922.0 | 
| Labview     | 2022-02-22 02:02:02 | 3728338194.0 |   

## The time

```python
from mcgpy.time import (tconvert, to_datetime, to_timestamp)
```
The `time` module consists of three converting methods:


| Functions        | Description         | 
|------------------|---------------------|
| [tconvert](https://pjjung.github.io/mcgpy/Classes/time.html#the-timetconvert) | Convert the timestamp (Unix or LabVIEW  type) to the datetime string, vice sersa | 
| [to_timestamp](https://pjjung.github.io/mcgpy/Classes/time.html#the-timeto_timestamp) | Convert the datetime string to the timestamp (Unix or LabVIEW  type) | 
| [to_datetime](https://pjjung.github.io/mcgpy/Classes/time.html#the-timeto_datetime) | Convert the the timestamp (Unix or LabVIEW  type) to the datetime string | 
 
