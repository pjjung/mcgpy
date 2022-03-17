---
sort: 2
---

# Encode and Decode Patient Informatnion

## The key

```python
from mcgpy.key import (encode, decode)
```

To protect personal information, MCGpy provides basic encryption methods that encode and decode a patient's name, birthday, and gender, respectively. Each function is contained in the [`key`](https://pjjung.github.io/mcgpy/Classes/key.html) module, and their references are the fowling below.

| Methods             | Description                   |
|---------------------|-------------------------------|
| [encode](https://pjjung.github.io/mcgpy/Classes/key.html#the-keyencode) | Encode personal nane, birthday, and gender | 
| [decode](https://pjjung.github.io/mcgpy/Classes/key.html#the-keydecode) | Decode personal information from the encrypted string | 
