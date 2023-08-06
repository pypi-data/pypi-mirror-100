# Pijavski

This package uses CFFI to call the function Pijavski written in C++ that optimises a test function and returns the minimum.


## Installation

To install simply type:

```
$ pip install pijavski
```


## Usage

To test, open a python console and import the package. The function `pijavski.get_minimum`, with arguments *lip*, *xl*, *xu*, *precision* and *maxiter*, prints `res`, `x0`, `f`, `prec`, `maxit` as result.

```
>>> import pijavski
>>> pijavski.get_minimum()
0 314.1592651760589 -0.9999999991415484 8.584516431042744e-10 65533
```

### Defining custom functions to optimise

The function to optimise needs to be declared following the conditions below:

- When writing the function,  arguments `f` and `x` need to be declared as if they were pointers using the bracket notation f[] and x[].

- Use numpy math functions.

- Modify the definition of the function `generic_fun` to received as argument the name of your custom function.


Example:

```    
>>> # Simple declaration of f = -cos^2(x) as callback function.
>>> import numpy as np
>>> from pijavski import get_minimum, ffi, lib
>>> def my_fun(x, f):
...     f[0] = (-1)*np.cos(x[0])**2
>>> def generic_fun(x, f, myfun=my_fun):
...     return myfun(x, f)
>>> # Call get_minimum
>>> get_minimum(func=lib.fun, xl=-100, xu=100)
0 -1.0 4.6838846e-317 4.6838846e-317 1 
```
