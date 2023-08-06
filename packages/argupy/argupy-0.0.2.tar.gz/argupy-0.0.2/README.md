# argupy
Easy-to-use argument manager for Python3.

## Instalation
To install argupy, run
```
pip3 install argupy
```

## Usage
To use it in a Python script, first you need to import it.
``` python
from argupy import *
```

Then, initialize the `Args` class
``` python
argupy = Args()
```
and define any parameters you'll want to use later on.
``` python
argupy.setarg('--testarg', BOOL)
```

The `setarg` function takes these parameters:
* **name**: the parameter name, for example, '--test'
* **type_**: the parameter type, pass a constant like `BOOL`, `STR`, or `FLOAT`
* **default_value**: the default value to return if the argument is not present. Defaults to `False` if the argument is of type `BOOL`.

To define an argument which takes a value, use the types `STR` or `FLOAT`. Then retreive it with the `Args.arg()` method.
``` python
argupy.setarg('--testarg', STR)

value = argupy.arg('--testarg')

print(type(value), value)
# Running this code like this: 
# python3 file.py --testarg "hello world"
# would output: <class 'str'> hello world
```

If the argument type is set to `STR`, the returned value will be of type `str`. And again, if the argument is of type `FLOAT`, the returned value will be of type `float`, so you don't have to pass it through `float()`. Unless the argument is not present and the default value you specify is not of the corresponding type.