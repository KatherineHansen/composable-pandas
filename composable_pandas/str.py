from composable import pipeable
import pandas as pd
import numpy as np

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
def get_dummies(col, sep="|"):
    """Split each string in the Series by sep and return a DataFrame
    of dummy/indicator variables.
    
    Parameters
    ----------
    sep : str, default "|"
        String to split on.
    
    Returns
    -------
    DataFrame
        Dummy variables corresponding to values of the Series.
    
    See Also
    --------
    get_dummies : Convert categorical variable into dummy/indicator
        variables.
    
    Examples
    --------
    >>> pd.Series(['a|b', 'a', 'a|c']) >> get_dummies()
       a  b  c
    0  1  1  0
    1  1  0  0
    2  1  0  1
    
    >>> pd.Series(['a|b', np.nan, 'a|c']) >> get_dummies()
       a  b  c
    0  1  1  0
    1  0  0  0
    2  1  0  1

    """
    return col.str.get_dummies(sep)
