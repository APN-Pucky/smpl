"""Simplified general utilities."""

import warnings

import numpy as np

from smpl import doc


def dict_unique_by_value(d: dict) -> dict:
    seen_ids = set()
    result = {}
    for key, value in d.items():
        value_id = id(value)
        if value_id not in seen_ids:
            result[key] = value
            seen_ids.add(value_id)
    return result


@doc.deprecated("1.0.3", "Use `s*n` instead.")
def times(s, n):
    """
    Concats string ``s`` ``n`` times.

    Examples
    --------
    >>> times("hi",5)
    'hihihihihi'

    .. deprecated:: 0.0.0

    """
    return s.join(["" for i in range(n + 1)])


# TODO make nicer transparent with fields?
def rename(old, new, warning=True):
    """
    Annotation to replace the name of a function argument.

    Examples
    --------
    >>> @rename("a","b")
    ... def f(b):
    ...     return b
    >>> f(1)
    1
    >>> f(a=1)
    1
    >>> f(b=1)
    1
    >>> f(b=2,a=1)
    2
    """

    def wrapper(target):
        def lammda(*args, **kwargs):
            if old in kwargs and new in kwargs:
                if warning:
                    warnings.warn(
                        f"Argument {old} and {new} are both set, {new} will be used.",
                        DeprecationWarning,
                    )
                del kwargs[old]
            elif old in kwargs:
                if warning:
                    warnings.warn(
                        f"Argument {old} is deprecated, use {new} instead.",
                        DeprecationWarning,
                    )
                kwargs[new] = kwargs[old]
                del kwargs[old]
            return target(*args, **kwargs)

        lammda.__doc__ = target.__doc__
        return lammda

    return wrapper


# TODO split in to own package
def withify(prefix="with_", sufix="", override=False):
    """
    Decorator to add with_ methods to a class.

    Examples
    --------

    >>> from dataclasses import dataclass, field
    >>> from typing import Optional
    >>> @withify()
    ... @dataclass
    ... class A:
    ...     a : Optional[int] = field(default=0)
    ...     b : Optional[int] = field(default=0)
    ...     c : Optional[int] = field(default=0)
    >>> a = A(0,0,0)
    >>> a.with_a(1).with_b(2).with_c(3)
    A(a=1, b=2, c=3)
    """

    def _withify(cls):
        inst = cls()
        for k in inst.__annotations__.keys():
            fun = prefix + k + sufix
            ok = k
            if override or not hasattr(cls, fun):

                def tmp(self, value, k=ok):
                    """Set `value` and return self."""
                    self.__dict__[k] = value
                    return self

                tmp.__doc__ = f"Set {k} to `value` and return self."
                setattr(cls, fun, tmp)
        return cls

    return _withify


def get(key, ddict, default=None):
    """
    Returns dict[key] if this exists else default.

    Examples
    --------
    >>> d = {'a' : 1 , 'b' : 2 , 'c' : 3}
    >>> get('a',d,5)
    1
    >>> get('x',d,5)
    5

    """
    if has(key, ddict):
        return ddict[key]
    return default


def has(key, ddict):
    """
    Checks if the key is in the dict and not None.

    Examples
    --------
    >>> d = {'a' : 1 , 'b' : 2 , 'c' : 3}
    >>> has('a',d)
    True
    >>> has('x',d)
    False


    """
    return key in ddict and ddict[key] is not None


def true(key, ddict):
    """
    Checks if the key is in the dict and not None and True.

    Examples
    --------
    >>> d = {'a' : True , 'b' : True , 'c' : False}
    >>> true('a', d)
    True
    >>> true('c', d)
    False
    >>> true('x', d)
    False

    """
    return has(key, ddict) and ddict[key]


def find_nearest_index(array, value):
    """
    Returns the index of the element in ``array`` closest to ``value``

    Examples
    --------
    >>> int(find_nearest_index([1,7,6,2] , 1.9))
    3

    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def find_nearest(array, value):
    """
    Return the element in ``array`` closest to ``value``

    Examples
    --------
    >>> find_nearest([1,7,6,2] , 1.9)
    2

    """
    return array[find_nearest_index(array, value)]
