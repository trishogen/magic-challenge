import pytest
from flatten_array.flatten_array import flatten_array


@pytest.mark.parametrize("test_input, expected", [
    ([1, 2, 3], [1, 2, 3]),  # a normal array of ints
    ([1, 'banana', 3], [1, 'banana', 3.0, ]),  # a normal array mixed data types
    ([1, [2, 3], 4, 5, [1]], [1, 2, 3, 4, 5, 1]),  # a non flat array of ints
    ([1, ['apple', 3], 4, {}, [7.0]], [1, 'apple', 3, 4, {}, 7.0]),  # a non flat array of mixed data types
    ([1, [[2], [3]], [4, 5, [[1]]]], [1, 2, 3, 4, 5, 1]),  # some other variations in nesting
    ([[[[[[[[[[[[[1]]]]]]]]]]]]], [1]),  # an extremely nested array
    ([[[]], []], [])  # a non-flat empty array
])
def test_flatten_array(test_input, expected):
    """Test that _flatten works within flatten_array"""
    assert flatten_array(test_input) == expected


def test_flatten_array_failure():
    """Test that an error will be thrown if something other than a list is passed in"""
    with pytest.raises(ValueError, match="Please pass in a valid array"):
        flatten_array("")
