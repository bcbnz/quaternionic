import functools
import numpy as np
import quaternionic
import pytest


def test_self_return():
    def f1(a, b, c):
        d = np.asarray(a).copy()
        assert isinstance(a, np.ndarray) and isinstance(a, quaternionic.array)
        assert isinstance(b, np.ndarray) and isinstance(b, quaternionic.array)
        assert isinstance(c, np.ndarray) and isinstance(c, quaternionic.array)
        assert isinstance(d, np.ndarray) and not isinstance(d, quaternionic.array)
        return d
    a = quaternionic.array(np.random.rand(17, 3, 4))
    b = quaternionic.array(np.random.rand(13, 3, 4))
    c = quaternionic.array(np.random.rand(11, 3, 4))
    d1 = f1(a, b, c)
    assert isinstance(d1, np.ndarray) and not isinstance(d1, quaternionic.array)
    f2 = quaternionic.utilities.type_self_return(f1)
    d2 = f2(a, b, c)
    assert isinstance(d2, np.ndarray) and isinstance(d2, quaternionic.array)
    f1.nin = 3
    f3 = quaternionic.utilities.type_self_return(f1)
    d3 = f3(a, b, c)
    assert isinstance(d3, np.ndarray) and isinstance(d3, quaternionic.array)


def test_ndarray_args():
    def f1(a, b, c):
        d = np.asarray(a).copy()
        assert isinstance(a, np.ndarray) and not isinstance(a, quaternionic.array)
        assert isinstance(b, np.ndarray) and not isinstance(b, quaternionic.array)
        assert isinstance(c, np.ndarray) and not isinstance(c, quaternionic.array)
        assert isinstance(d, np.ndarray) and not isinstance(d, quaternionic.array)
        return d
    a = quaternionic.array(np.random.rand(17, 3, 4))
    b = quaternionic.array(np.random.rand(13, 3, 4))
    c = quaternionic.array(np.random.rand(11, 3, 4))
    f2 = quaternionic.utilities.ndarray_args(f1)
    d2 = f2(a, b, c)
    assert isinstance(d2, np.ndarray) and not isinstance(d2, quaternionic.array)
    f1.nin = 3
    f3 = quaternionic.utilities.ndarray_args(f1)
    d3 = f3(a, b, c)
    assert isinstance(d3, np.ndarray) and not isinstance(d3, quaternionic.array)


def test_ndarray_args_and_return():
    def f1(a, b, c):
        d = np.asarray(a).copy()
        assert isinstance(a, np.ndarray) and not isinstance(a, quaternionic.array)
        assert isinstance(b, np.ndarray) and not isinstance(b, quaternionic.array)
        assert isinstance(c, np.ndarray) and not isinstance(c, quaternionic.array)
        assert isinstance(d, np.ndarray) and not isinstance(d, quaternionic.array)
        return d
    a = quaternionic.array(np.random.rand(17, 3, 4))
    b = quaternionic.array(np.random.rand(13, 3, 4))
    c = quaternionic.array(np.random.rand(11, 3, 4))
    f2 = quaternionic.utilities.ndarray_args_and_return(f1)
    d2 = f2(a, b, c)
    assert isinstance(d2, np.ndarray) and isinstance(d2, quaternionic.array)
    f1.nin = 3
    f3 = quaternionic.utilities.ndarray_args_and_return(f1)
    d3 = f3(a, b, c)
    assert isinstance(d3, np.ndarray) and isinstance(d3, quaternionic.array)


def test_types_to_ftylist():
    import numba
    types_to_ftylist = quaternionic.utilities.convert_numpy_ufunc_type_to_numba_ftylist
    types = '?bhilqpBHILQPfdgF->D'
    ftylist = numba.complex128(
        numba.boolean,
        numba.byte,
        numba.short,
        numba.intc,
        numba.int_,
        numba.longlong,
        numba.intp,
        numba.char,
        numba.ushort,
        numba.uintc,
        numba.uint,
        numba.ulonglong,
        numba.uintp,
        numba.float32,
        numba.float_,
        numba.double,
        numba.complex64,
    )
    assert types_to_ftylist([types]) == [ftylist]


def test_pyguvectorize():
    x = quaternionic.array(np.random.rand(7, 13, 4))
    y = quaternionic.array(np.random.rand(13, 4))
    z = np.random.rand(13)

    for k in dir(quaternionic.algebra_ufuncs):
        if not k.startswith('__'):
            f1 = getattr(quaternionic.algebra_ufuncs, k)
            f2 = getattr(quaternionic.algebra, k)
            sig = f2.signature
            inputs = sig.split('->')[0].split(',')
            args = [x.ndarray] if inputs[0] == '(n)' else [z,]
            if len(inputs) > 1:
                args.append(y.ndarray if inputs[1] == '(n)' else z)
            assert np.array_equal(quaternionic.utilities.pyguvectorize(f2)(*args), f1(*args))