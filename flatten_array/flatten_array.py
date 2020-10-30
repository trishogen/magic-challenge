"""Question 4"""


def flatten_array(hopefully_a_list):
    """ Flattens arrays, but makes sure that they are of list type"""
    if not isinstance(hopefully_a_list, list):
        # The starting argument was not a list, or one of the items nested in the list was not a list
        raise ValueError('Please pass in a valid array')

    return _flatten(hopefully_a_list)


def _flatten(lst):
    """ Takes an array and flattens it"""
    if isinstance(lst, list) and not lst:
        return lst  # base case: if it is an empty list return it
    if isinstance(lst[0], list):
        # if the first element is a list, call flatten on the first element then add it to flatten(rest of the elements)
        return _flatten(lst[0]) + _flatten(lst[1:])

    return lst[:1] + _flatten(lst[1:])  # otherwise return the first element, + flatten(the rest)


if __name__ == '__main__':
    print(flatten_array([[1, 2, [3]], 4]))
