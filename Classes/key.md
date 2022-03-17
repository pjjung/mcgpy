---
sort: 6
---

# key

```python
from mcgpy.key import (encode, decode)
```

## Functions sumarry

| Functions | Description |
|-----------|-------------|
| [encode(patient_name, gender, birth_date)](https://pjjung.github.io/mcgpy/Classes/key.html#the-keyencode) | Encode personal name, birthday, and gender |
| [decode(name)](https://pjjung.github.io/mcgpy/Classes/key.html#the-keydecode) | Decode personal information from the encrypted string |

## The key.encode

*def* **mcgpy.key.encode**(patient_name, gender, birth_date, *args, **kwargs)

### Parameters

* **patient_name** : `str`

  patient's name

* **gender** : `str`

  patient's gender

* **birth_date** : `str`

  patient's bith date

### Raise

* **ValueError**

  * if the input gender argument is no valid string, "man", "woman", "male", "female", 0, or 1
  * if the input birth_data argument does not match to valid format, `%Y-%m-%d %H:%M:%S`

### Return : `tuple`

* **fianlencoded name** : `str`

  output of encoded information

* **folder name** : `str`

  output of encoded information with current date

### Examples

```python
>>> from mcgpy.key import encode
>>> encode("phil", "male", "2222-02-22 22:22:22")
  ("a7576ae32B2566A8F16F", "a7F76ae32B2566A8F165_22221223'")
```

---

## The key.decode

*def* **mcgpy.key.decode**(name, *args, **kwargs)

### Parameters

* **name** : `str`

  encoded string

### Raise

* **NameError**

  if the input string is no valid name

```warning
**OverflowError**

The error was reported in some environments if the `time` module tries to convert the timestamp before the Unix epoch standard to the `datetime.datetime` format.
```

### Return : `dict`

```python
dict{"patient name" : decoded patient's name from an input string
     "gender" : decoded patient's gender from an input string
     "birth date" : decoded patient's birth date from an input string as "datetime.datetime" 
     }
```

### Examples

```python
>>> from mcgpy.key import decode
>>> decode("a7576ae32B2566A8F16F")
{'patient name': 'phil',
 'gender': 'Male',
 'birth date': datetime.datetime(2222, 2, 22, 22, 22, 22)}
```
