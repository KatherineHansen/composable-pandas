from composable import pipeable
import pandas as pd
import numpy as np



@pipeable
def asfreq(col, *, args = tuple([]), **kwargs):
    """Convert the Period Array/Index to the specified frequency `freq`.
    
    Parameters
    ----------
    freq : str
        A frequency.
    how : str {'E', 'S'}
        Whether the elements should be aligned to the end
        or start within pa period.
    
        * 'E', 'END', or 'FINISH' for end,
        * 'S', 'START', or 'BEGIN' for start.
    
        January 31st ('END') vs. January 1st ('START') for example.
    
    Returns
    -------
    Period Array/Index
        Constructed with the new frequency.
    
    Examples
    --------
    >>> pidx = pd.Series(pd.period_range('2010-01-01', '2015-01-01', freq='A'))
    >>> pidx
    0    2010
    1    2011
    2    2012
    3    2013
    4    2014
    5    2015
    dtype: period[A-DEC]
    
    >>> pidx >> asfreq(args = ['M'])
    0    2010-12
    1    2011-12
    2    2012-12
    3    2013-12
    4    2014-12
    5    2015-12
    dtype: period[M]
    
    >>> pidx >> asfreq(args = ['M'], how='S')
    0    2010-01
    1    2011-01
    2    2012-01
    3    2013-01
    4    2014-01
    5    2015-01
    dtype: period[M]
    """
    return col.dt.asfreq(*args, **kwargs)

@pipeable
def ceil(col, *, args = tuple([]), **kwargs):
    """Perform ceil operation on the data to the specified `freq`.
    
    Parameters
    ----------
    freq : str or Offset
        The frequency level to ceil the index to. Must be a fixed
        frequency like 'S' (second) not 'ME' (month end). See
        :ref:`frequency aliases <timeseries.offset_aliases>` for
        a list of possible `freq` values.
    ambiguous : 'infer', bool-ndarray, 'NaT', default 'raise'
        Only relevant for DatetimeIndex:
    
        - 'infer' will attempt to infer fall dst-transition hours based on
          order
        - bool-ndarray where True signifies a DST time, False designates
          a non-DST time (note that this flag is only applicable for
          ambiguous times)
        - 'NaT' will return NaT where there are ambiguous times
        - 'raise' will raise an AmbiguousTimeError if there are ambiguous
          times.
    
        .. versionadded:: 0.24.0
    
    nonexistent : 'shift_forward', 'shift_backward', 'NaT', timedelta, default 'raise'
        A nonexistent time does not exist in a particular timezone
        where clocks moved forward due to DST.
    
        - 'shift_forward' will shift the nonexistent time forward to the
          closest existing time
        - 'shift_backward' will shift the nonexistent time backward to the
          closest existing time
        - 'NaT' will return NaT where there are nonexistent times
        - timedelta objects will shift nonexistent times by the timedelta
        - 'raise' will raise an NonExistentTimeError if there are
          nonexistent times.
    
        .. versionadded:: 0.24.0
    
    Returns
    -------
    DatetimeIndex, TimedeltaIndex, or Series
        Index of the same type for a DatetimeIndex or TimedeltaIndex,
        or a Series with the same index for a Series.
    
    Raises
    ------
    ValueError if the `freq` cannot be converted.
    
    Examples
    --------
    **DatetimeIndex**
    
    >>> rng = pd.date_range('1/1/2018 11:59:00', periods=3, freq='min')
    
    **Series**
    
    >>> pd.Series(rng) >> ceil(args=["H"])
    0   2018-01-01 12:00:00
    1   2018-01-01 12:00:00
    2   2018-01-01 13:00:00
    dtype: datetime64[ns]
    """
    return col.dt.ceil(*args, **kwargs)

@pipeable
def to_timestamp(col, *, args = tuple([]), **kwargs):
#def to_timestamp(args, col, **kwargs):
    """Cast to DatetimeArray/Index.
    
    Parameters
    ----------
    freq : str or DateOffset, optional
        Target frequency. The default is 'D' for week or longer,
        'S' otherwise.
    how : {'s', 'e', 'start', 'end'}
        Whether to use the start or end of the time period being converted.
    
    Returns
    -------
    DatetimeArray/Index
    """
    return col.dt.to_timestamp(*args, **kwargs)

@pipeable
def total_seconds(col, *, args = tuple([]), **kwargs):
    """Return total duration of each element expressed in seconds.
    
    This method is available directly on TimedeltaArray, TimedeltaIndex
    and on Series containing timedelta values under the ``.dt`` namespace.
    
    Returns
    -------
    seconds : [ndarray, Float64Index, Series]
        When the calling object is a TimedeltaArray, the return type
        is ndarray.  When the calling object is a TimedeltaIndex,
        the return type is a Float64Index. When the calling object
        is a Series, the return type is Series of type `float64` whose
        index is the same as the original.
    
    See Also
    --------
    datetime.timedelta.total_seconds : Standard library version
        of this method.
    TimedeltaIndex.components : Return a DataFrame with components of
        each Timedelta.
    
    Examples
    --------
    **Series**
    
    >>> s = pd.Series(pd.to_timedelta(np.arange(5), unit='d'))
    >>> s
    0   0 days
    1   1 days
    2   2 days
    3   3 days
    4   4 days
    dtype: timedelta64[ns]
    
    >>> s >> total_seconds()
    0         0.0
    1     86400.0
    2    172800.0
    3    259200.0
    4    345600.0
    dtype: float64
    """
    return col.dt.total_seconds(*args, **kwargs)

@pipeable
def tz_localize(col, *, args = tuple([]), **kwargs):
    """Localize tz-naive Datetime Array/Index to tz-aware
    Datetime Array/Index.
    
    This method takes a time zone (tz) naive Datetime Array/Index object
    and makes this time zone aware. It does not move the time to another
    time zone.
    Time zone localization helps to switch from time zone aware to time
    zone unaware objects.
    
    Parameters
    ----------
    tz : str, pytz.timezone, dateutil.tz.tzfile or None
        Time zone to convert timestamps to. Passing ``None`` will
        remove the time zone information preserving local time.
    ambiguous : 'infer', 'NaT', bool array, default 'raise'
        When clocks moved backward due to DST, ambiguous times may arise.
        For example in Central European Time (UTC+01), when going from
        03:00 DST to 02:00 non-DST, 02:30:00 local time occurs both at
        00:30:00 UTC and at 01:30:00 UTC. In such a situation, the
        `ambiguous` parameter dictates how ambiguous times should be
        handled.
    
        - 'infer' will attempt to infer fall dst-transition hours based on
          order
        - bool-ndarray where True signifies a DST time, False signifies a
          non-DST time (note that this flag is only applicable for
          ambiguous times)
        - 'NaT' will return NaT where there are ambiguous times
        - 'raise' will raise an AmbiguousTimeError if there are ambiguous
          times.
    
    nonexistent : 'shift_forward', 'shift_backward, 'NaT', timedelta, default 'raise'
        A nonexistent time does not exist in a particular timezone
        where clocks moved forward due to DST.
    
        - 'shift_forward' will shift the nonexistent time forward to the
          closest existing time
        - 'shift_backward' will shift the nonexistent time backward to the
          closest existing time
        - 'NaT' will return NaT where there are nonexistent times
        - timedelta objects will shift nonexistent times by the timedelta
        - 'raise' will raise an NonExistentTimeError if there are
          nonexistent times.
    
        .. versionadded:: 0.24.0
    
    Returns
    -------
    Same type as self
        Array/Index converted to the specified time zone.
    
    Raises
    ------
    TypeError
        If the Datetime Array/Index is tz-aware and tz is not None.
    
    See Also
    --------
    DatetimeIndex.tz_convert : Convert tz-aware DatetimeIndex from
        one time zone to another.
    
    Examples
    --------
    >>> tz_naive = pd.date_range('2018-03-01 09:00', periods=3)
    >>> tz_naive
    DatetimeIndex(['2018-03-01 09:00:00', '2018-03-02 09:00:00',
                   '2018-03-03 09:00:00'],
                  dtype='datetime64[ns]', freq='D')
    
    Localize DatetimeIndex in US/Eastern time zone:
    
    >>> tz_aware = pd.Series(tz_naive) >> tz_localize(tz='US/Eastern')
    >>> tz_aware
    0   2018-03-01 09:00:00-05:00
    1   2018-03-02 09:00:00-05:00
    2   2018-03-03 09:00:00-05:00
    dtype: datetime64[ns, US/Eastern]
    
    With the ``tz=None``, we can remove the time zone information
    while keeping the local time (not converted to UTC):
    
    >>> tz_aware >> tz_localize(args=[None])
    0   2018-03-01 09:00:00
    1   2018-03-02 09:00:00
    2   2018-03-03 09:00:00
    dtype: datetime64[ns]
    
    Be careful with DST changes. When there is sequential data, pandas can
    infer the DST time:
    
    >>> s = pd.to_datetime(pd.Series(['2018-10-28 01:30:00',
    ...                               '2018-10-28 02:00:00',
    ...                               '2018-10-28 02:30:00',
    ...                               '2018-10-28 02:00:00',
    ...                               '2018-10-28 02:30:00',
    ...                               '2018-10-28 03:00:00',
    ...                               '2018-10-28 03:30:00']))
    >>> s >> tz_localize(args=['CET'], ambiguous='infer')
    0   2018-10-28 01:30:00+02:00
    1   2018-10-28 02:00:00+02:00
    2   2018-10-28 02:30:00+02:00
    3   2018-10-28 02:00:00+01:00
    4   2018-10-28 02:30:00+01:00
    5   2018-10-28 03:00:00+01:00
    6   2018-10-28 03:30:00+01:00
    dtype: datetime64[ns, CET]
    
    In some cases, inferring the DST is impossible. In such cases, you can
    pass an ndarray to the ambiguous parameter to set the DST explicitly
    
    
    
    If the DST transition causes nonexistent times, you can shift these
    dates forward or backwards with a timedelta object or `'shift_forward'`
    or `'shift_backwards'`.
    
    >>> s = pd.to_datetime(pd.Series(['2015-03-29 02:30:00',
    ...                               '2015-03-29 03:30:00']))
    >>> s >> tz_localize(args=['Europe/Warsaw'], nonexistent='shift_forward')
    0   2015-03-29 03:00:00+02:00
    1   2015-03-29 03:30:00+02:00
    dtype: datetime64[ns, Europe/Warsaw]
    >>> s >> tz_localize(args=['Europe/Warsaw'], nonexistent='shift_backward')
    0   2015-03-29 01:59:59.999999999+01:00
    1   2015-03-29 03:30:00+02:00
    dtype: datetime64[ns, Europe/Warsaw]
    >>> s >> tz_localize(args=['Europe/Warsaw'], nonexistent=pd.Timedelta('1H'))
    0   2015-03-29 03:30:00+02:00
    1   2015-03-29 03:30:00+02:00
    dtype: datetime64[ns, Europe/Warsaw]
    """
    return col.dt.tz_localize(*args, **kwargs)