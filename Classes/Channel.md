---
sort: 5
---

# Channel

## The channel.ChannelConfig

*class* **mcgpy.channel.ChannelConfig**(path)

Read the information of sensor posirion, direction, number and label from a channel configuration file.

### Parameters

* **path** : `str`

  input path must be .ini format and include sensor information of MCG syste

### Raises

* **IOError**

  if a "str" input is not a configuration file path

* **TypeError**

  if a configuration file did not match a specific format

### Methods Summary

| Methods        | Discription |
|----------------|-------------|
| [get(key)](https://pjjung.github.io/mcgpy/Classes/Chaeenl.html#getkey)      | Provide the information by the given key         |

### Methods Documentation

#### get(key)

*def* **mcgpy.channel.ChannelConfig**.get(key)

Provide the information by the given key

##### Parameters

* **key** : `str`

  the key takes "Label", "Position", or "Positions"

##### Return : `astropy.table.QTable`

the sensor information as astropy QTable
  
##### Examples

```python
>>> from mcgpy.channel import ChannelConfig
>>> config = ChanngelConfig('~/test/file/path.ini')
>>> config.get("label")
number	label
int64	str3
1	    label_1
2	    label_2
3	    label_3
.
.
.
    
>>> config.get("positions")
number	positions
int64	float64
1	    (x1, y1, z1)
2	    (x2, y2, z2)
3	    (x3, y3, z3)
.
.
.
```

---

## The channel.ChannelActive

*class* **mcgpy.channel.ChannelActive**(path)

Read the information of active sensor number and label from raw files, for raw files contained active channel data only.

### Parameters

* **path** : `str`

  input path must be .kdf or .hdf5 format

### Raises

* **IOError**

  if a `str` input is not a raw file path: `.kdf` or `.hdf5`

### Methods Summary

| Methods        | Discription |
|----------------|-------------|
| [get_table()](https://pjjung.github.io/mcgpy/Classes/Chaeenl.html#get_table)      | Provide activie channel's number and label as `astropy.tabel.QTable` |
| [get_number()](https://pjjung.github.io/mcgpy/Classes/Chaeenl.html#get_number)      | Provide active channel's number as `list` |
| [get_label()](https://pjjung.github.io/mcgpy/Classes/Chaeenl.html#get_label)      | Provide active channel's label as `list` |

### Methods Documentation

#### get_table()

*def* **mcgpy.channel.ChannelActive**.get_table()

Provide activie channel's number and label as `astropy.tabel.QTable`

##### Return : `astropy.table.QTable`

the active sensor information as astropy QTable 
  
##### Examples

```python
>>> from mcgpy.channel import ChannelActive
>>> activated = ChannelActive("~/test/raw/file/path.hdf5")
>>> activated.get_table()
number	label
int64	str3
1	    label_1
2	    label_2
4	    label_4
10	    label_10
11	    label_11
.
.  
```

---

#### get_number()

*def* **mcgpy.channel.ChannelActive**.get_number()

Provide active channel's number as `list`

##### Return : `list`

the active sensor's number as list 
  
##### Examples

```python
>>> from mcgpy.channel import ChannelActive
>>> activated = ChannelActive("~/test/raw/file/path.hdf5")
>>> activated.get_number()
[1,2,4,10,11,...]
```
---

#### get_label()

*def* **mcgpy.channel.ChannelActive**.get_label()

Provide active channel's number as `list`

##### Return : `list`

the active sensor's label as list 
  
##### Examples

```python
>>> from mcgpy.channel import ChannelActive
>>> activated = ChannelActive("~/test/raw/file/path.hdf5")
>>> activated.get_label()
[label_1,label_2,label_4,label_10,label_11,...]
```
---
