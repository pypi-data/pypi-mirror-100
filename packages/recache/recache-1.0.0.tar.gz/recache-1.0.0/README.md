# recache

Cache functions to speed up recursion

## install

From Pypi:

`python -m pip install recache`

From GitHub:

`python -m pip install git+https://github.com/donno2048/recache`

## Usage

```py
from recache import cache
def fib(n): # slow recursion
    if n < 0: return None
    if n <= 1: return 1
    return fib(n - 1) + fib(n - 2)
@cache
def cfib(n): # fast recursion
    if n < 0: return None
    if n <= 1: return 1
    return cfib(n - 1) + cfib(n - 2)
```

To see the exact timing see [The notebook](https://github.com/donno2048/recache/blob/master/fib.ipynb)
