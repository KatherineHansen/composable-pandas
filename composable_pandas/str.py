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
def findall(pat, col, flags=0, **kwargs):
    """Find all occurrences of pattern or regular expression in the Series/Index.
    
    Equivalent to applying :func:`re.findall` to all the elements in the
    Series/Index.
    
    Parameters
    ----------
    pat : str
        Pattern or regular expression.
    flags : int, default 0
        Flags from ``re`` module, e.g. `re.IGNORECASE` (default is 0, which
        means no flags).
    
    Returns
    -------
    Series/Index of lists of strings
        All non-overlapping matches of pattern or regular expression in each
        string of this Series/Index.
    
    See Also
    --------
    count : Count occurrences of pattern or regular expression in each string
        of the Series/Index.
    extractall : For each string in the Series, extract groups from all matches
        of regular expression and return a DataFrame with one row for each
        match and one column for each group.
    re.findall : The equivalent ``re`` function to all non-overlapping matches
        of pattern or regular expression in string, as a list of strings.
    
    Examples
    --------
    
    >>> s = pd.Series(['Lion', 'Monkey', 'Rabbit'])
    
    The search for the pattern 'Monkey' returns one match:
    
    >>> s >> findall('Monkey')
    0          []
    1    [Monkey]
    2          []
    dtype: object
    
    On the other hand, the search for the pattern 'MONKEY' doesn't return any
    match:
    
    >>> s >> findall('MONKEY')
    0    []
    1    []
    2    []
    dtype: object
    
    Flags can be added to the pattern or regular expression. For instance,
    to find the pattern 'MONKEY' ignoring the case:
    
    >>> import re
    >>> s >> findall('MONKEY', flags=re.IGNORECASE)
    0          []
    1    [Monkey]
    2          []
    dtype: object
    
    When the pattern matches more than one string in the Series, all matches
    are returned:
    
    >>> s >> findall('on')
    0    [on]
    1    [on]
    2      []
    dtype: object
    
    Regular expressions are supported too. For instance, the search for all the
    strings ending with the word 'on' is shown next:
    
    >>> s >> findall('on$')
    0    [on]
    1      []
    2      []
    dtype: object
    
    If the pattern is found more than once in the same string, then a list of
    multiple strings is returned:
    
    >>> s >> findall('b')
    0        []
    1        []
    2    [b, b]
    dtype: object
    """
    return col.str.findall(pat, flags=0, **kwargs)