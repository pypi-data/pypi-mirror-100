# Pijavski

This is an example of how to use CFFI to call a Pijavski function written in C++ that optimises a test function and returns the minimum.


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
0 -5323.428786928975 1.2546522006214123e-09 3.5218863499790176 65533
```

### Defining custom functions to optimise

The function to optimise needs to be declared as a callback function for CFFI so that the Pijavski program can process it. The user can implement up to 20 functions following the conditions below:
    
- The function definition needs to be preceeded by `@ffi.def_extern()`.

- The function name must be `fun[1-20]` (suffix between 1 and 20) as this is how the callback function is defined in the CFFI builder.

- When writing the function,  arguments `f` and `x` need to be declared as if they were pointers using the bracket notation f[] and x[].

- Use numpy math functions.


Example:

```    
>>> import numpy as np
>>> from pijavski import get_minimum, ffi, lib
>>> # Simple declaration of f = -cos^2(x) as callback function.
>>> @ffi.def_extern()
... def fun1(f, x):
...     f[0] = (-1)*np.cos(x[0])**2
>>> # Simple declaration of f = sin^2(x) as callback function.
>>> @ffi.def_extern()
... def fun2(f, x):
...     f[0] = np.sin(x[0])**2
>>> # Call get_minimum for fun1
>>> get_minimum(func=lib.fun1, xl=-100, xu=100)
0 -1.0 4.6838846e-317 4.6838846e-317 1 
>>> # Call get_minimum for fun2
>>> get_minimum(func=lib.fun2, xl=-100, xu=100)
0 -1.0 4.6838846e-317 4.6838846e-317 1 
```
