# The test is from https://github.com/SirAnthony/slpp

import rookout.lua as lua
import os

def setup():
    pass

def is_iterator(obj):
    """
    >>> assert is_iterator(list()) is True
    >>> assert is_iterator(int) is False
    """
    if isinstance(obj, (list, tuple)):
        return True
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def test_iterator():
    assert is_iterator(list()) is True
    assert is_iterator(int) is False

def test_decode_file():
    luafile = os.path.join(os.path.split(__file__)[0], 'ani_def_sample.lua')
    adict = lua.decode_file(luafile)
    assert len(adict['spritesheets']) == 2

def differ(value, origin):
    """
    Same:
    >>> differ(1, 1)
    >>> differ([2, 3], [2, 3])
    >>> differ({'1': 3, '4': '6'}, {'4': '6', '1': 3})
    >>> differ('4', '4')

    Different:
    >>> differ(1, 2)
    Traceback (most recent call last):
       ...
    AssertionError: 1 not match original: 2.
    >>> differ([2, 3], [3, 2])
    Traceback (most recent call last):
       ...
    AssertionError: 2 not match original: 3.
    >>> differ({'6': 4, '3': '1'}, {'4': '6', '1': 3})
    Traceback (most recent call last):
       ...
    AssertionError: {'3': '1', '6': 4} not match original: {'1': 3, '4': '6'};
    Key: 1, item: 3
    >>> differ('4', 'no')
    Traceback (most recent call last):
       ...
    AssertionError: 4 not match original: no.
    """

    if type(value) is not type(origin):
        raise AssertionError('Types does not match: {0}, {1}'.format(type(value), type(origin)))

    if isinstance(origin, dict):
        for key, item in origin.items():
            try:
                differ(value[key], item)
            except KeyError:
                raise AssertionError('''{0} not match original: {1};
Key: {2}, item: {3}'''.format(value, origin, key, item))
            return

    if isinstance(origin, str):
        assert value == origin, '{0} not match original: {1}.'.format(value, origin)
        return

    if is_iterator(origin):
        for i in range(0, len(origin)):
            try:
                differ(value[i], origin[i])
            except IndexError:
                raise AssertionError(
                    '{0} not match original: {1}. Item {2} not found'.format(
                        response, origin, origin[i]))
            except Exception as e:
                raise e
        return

    assert value == origin, '{0} not match original: {1}.'.format(value, origin)



def number_test():
    """
    Integer and float:
    >>> assert lua.decode('3') == 3
    >>> assert lua.decode('4.1') == 4.1

    Negative float:
    >>> assert lua.decode('-0.45') == -0.45

    Scientific:
    >>> assert lua.decode('3e-7') == 3e-7
    >>> assert lua.decode('-3.23e+17') == -3.23e+17

    Hex:
    >>> assert lua.decode('0x3a') == 0x3a

    #4
    >>> differ(lua.decode('''{      \
        ID = 0x74fa4cae,            \
        Version = 0x07c2,           \
        Manfacturer = 0x21544948    \
    }'''), {                        \
        'ID': 0x74fa4cae,           \
        'Version': 0x07c2,          \
        'Manufacturer': 0x21544948  \
    })
    """
    pass

def table_test():
    """
    Bracketed string key:
    >>> assert lua.decode('{[10] = 1}') == {10: 1}

    Void table:
    >>> assert lua.decode('{nil}') == []

    Values-only table:
    >>> assert lua.decode('{"10"}') == ["10"]
    """
    pass

def string_test():
    r"""
    Escape test:
    >>> assert lua.decode(r"'test\'s string'") == "test's string"

    Add escaping on encode:
    >>> assert lua.encode({'a': 'func("call()");'}) == '{\n\ta = "func(\\"call()\\");"\n}'
    """
    pass

def basic_test():
    """
    No data loss:

    >>> data = '{ array = { 65, 23, 5 }, dict = { string = "value", array = { 3, 6, 4}, mixed = { 43, 54.3, false, string = "value", 9 } } }'
    >>> d = lua.decode(data)
    >>> differ(d, lua.decode(lua.encode(d)))
    """
    pass

