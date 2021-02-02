from composable import pipeable
import pandas as pd


@pipeable
def capitalize(col):
    """Convert strings in the Series/Index to be capitalized.
    
    Equivalent to :meth:`str.capitalize`.
    
    Returns
    -------
    Series or Index of object
    
    See Also
    --------
    str.lower : Converts all characters to lowercase.
    str.upper : Converts all characters to uppercase.
    str.title : Converts first character of each word to uppercase and
        remaining to lowercase.
    str.capitalize : Converts first character to uppercase and
        remaining to lowercase.
    str.swapcase : Converts uppercase to lowercase and lowercase to
        uppercase.
    str.casefold: Removes all case distinctions in the string.
    
    Examples
    --------
    >>> s = pd.Series(['lower', 'CAPITALS', 'this is a sentence', 'SwApCaSe'])
    >>> s
    0                 lower
    1              CAPITALS
    2    this is a sentence
    3              SwApCaSe
    dtype: object
    
    >>> s >> capitalize
    0                 Lower
    1              Capitals
    2    This is a sentence
    3              Swapcase
    dtype: object
    
    """
    return col.str.capitalize()


@pipeable
def get(i, col):
    """Extract element from each component at specified position.
    
    Extract element from lists, tuples, or strings in each element in the
    Series/Index.
    
    Parameters
    ----------
    i : int
        Position of element to extract.
    
    Returns
    -------
    Series or Index
    
    Examples
    --------
    >>> s = pd.Series(["String",
    ...               (1, 2, 3),
    ...               ["a", "b", "c"],
    ...               123,
    ...               -456,
    ...               {1: "Hello", "2": "World"}])
    >>> s
    0                        String
    1                     (1, 2, 3)
    2                     [a, b, c]
    3                           123
    4                          -456
    5    {1: 'Hello', '2': 'World'}
    dtype: object
    
    >>> s >> get(1)
    0        t
    1        2
    2        b
    3      NaN
    4      NaN
    5    Hello
    dtype: object
    
    >>> s >> get(-1)
    0      g
    1      3
    2      c
    3    NaN
    4    NaN
    5    None
    dtype: object
    """
    return col.str.get(i)