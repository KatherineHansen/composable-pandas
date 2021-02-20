from composable_pandas.str import asfreq, ceil, to_timestamp, total_seconds, tz_localize

import numpy as np
import pytest
import pandas as pd

from pandas import Series, _testing as tm
from pandas import DataFrame, DatetimeIndex, Series, date_range, period_range , Timestamp, Period, TimedeltaIndex
from pandas.tseries.offsets import BDay, BMonthEnd
from pandas._libs.tslibs import NaT, Timedelta, Timestamp, conversion
from pandas.core.arrays import DatetimeArray, TimedeltaArray
from datetime import datetime


def test_asfreq():
    pi1 = pd.Series(period_range(freq="A", start="1/1/2001", end="1/1/2001"))
    pi2 = pd.Series(period_range(freq="Q", start="1/1/2001", end="1/1/2001"))
    pi3 = pd.Series(period_range(freq="M", start="1/1/2001", end="1/1/2001"))
    pi4 = pd.Series(period_range(freq="D", start="1/1/2001", end="1/1/2001"))
    pi5 = pd.Series(period_range(freq="H", start="1/1/2001", end="1/1/2001 00:00"))
    pi6 = pd.Series(period_range(freq="Min", start="1/1/2001", end="1/1/2001 00:00"))
    pi7 = pd.Series(period_range(freq="S", start="1/1/2001", end="1/1/2001 00:00:00"))

    tm.assert_series_equal(pi1 >> asfreq(args=["Q", "S"]), pi2)
    tm.assert_series_equal(pi1 >> asfreq(args=["Q", "S"]), pi2)
    tm.assert_series_equal(pi1 >> asfreq(args=["M", "start"]), pi3)
    tm.assert_series_equal(pi1 >> asfreq(args=["D", "StarT"]), pi4)
    tm.assert_series_equal(pi1 >> asfreq(args=["H", "beGIN"]), pi5)
    tm.assert_series_equal(pi1 >> asfreq(args=["Min", "S"]), pi6)
    tm.assert_series_equal(pi1 >> asfreq(args=["S", "S"]), pi7)

    tm.assert_series_equal(pi2 >> asfreq(args=["M", "S"]), pi3)
    tm.assert_series_equal(pi2 >> asfreq(args=["D", "S"]), pi4)
    tm.assert_series_equal(pi2 >> asfreq(args=["H", "S"]), pi5)
    tm.assert_series_equal(pi2 >> asfreq(args=["Min", "S"]), pi6)
    tm.assert_series_equal(pi2 >> asfreq(args=["S", "S"]), pi7)

    tm.assert_series_equal(pi3 >> asfreq(args=["A", "S"]), pi1)
    tm.assert_series_equal(pi3 >> asfreq(args=["Q", "S"]), pi2)
    tm.assert_series_equal(pi3 >> asfreq(args=["D", "S"]), pi4)
    tm.assert_series_equal(pi3 >> asfreq(args=["H", "S"]), pi5)
    tm.assert_series_equal(pi3 >> asfreq(args=["Min", "S"]), pi6)
    tm.assert_series_equal(pi3 >> asfreq(args=["S", "S"]), pi7)

    tm.assert_series_equal(pi4 >> asfreq(args=["A", "S"]), pi1)
    tm.assert_series_equal(pi4 >> asfreq(args=["Q", "S"]), pi2)
    tm.assert_series_equal(pi4 >> asfreq(args=["M", "S"]), pi3)
    tm.assert_series_equal(pi4 >> asfreq(args=["H", "S"]), pi5)
    tm.assert_series_equal(pi4 >> asfreq(args=["Min", "S"]), pi6)
    tm.assert_series_equal(pi4 >> asfreq(args=["S", "S"]), pi7)

    tm.assert_series_equal(pi5 >> asfreq(args=["A", "S"]), pi1)
    tm.assert_series_equal(pi5 >> asfreq(args=["Q", "S"]), pi2)
    tm.assert_series_equal(pi5 >> asfreq(args=["M", "S"]), pi3)
    tm.assert_series_equal(pi5 >> asfreq(args=["D", "S"]), pi4)
    tm.assert_series_equal(pi5 >> asfreq(args=["Min", "S"]), pi6)
    tm.assert_series_equal(pi5 >> asfreq(args=["S", "S"]), pi7)

    tm.assert_series_equal(pi6 >> asfreq(args=["A", "S"]), pi1)
    tm.assert_series_equal(pi6 >> asfreq(args=["Q", "S"]), pi2)
    tm.assert_series_equal(pi6 >> asfreq(args=["M", "S"]), pi3)
    tm.assert_series_equal(pi6 >> asfreq(args=["D", "S"]), pi4)
    tm.assert_series_equal(pi6 >> asfreq(args=["H", "S"]), pi5)
    tm.assert_series_equal(pi6 >> asfreq(args=["S", "S"]), pi7)

    tm.assert_series_equal(pi7 >> asfreq(args=["A", "S"]), pi1)
    tm.assert_series_equal(pi7 >> asfreq(args=["Q", "S"]), pi2)
    tm.assert_series_equal(pi7 >> asfreq(args=["M", "S"]), pi3)
    tm.assert_series_equal(pi7 >> asfreq(args=["D", "S"]), pi4)
    tm.assert_series_equal(pi7 >> asfreq(args=["H", "S"]), pi5)
    tm.assert_series_equal(pi7 >> asfreq(args=["Min", "S"]), pi6)

    msg = "How must be one of S or E"
    with pytest.raises(ValueError, match=msg):
        pi7 >> asfreq(args=["T", "foo"])
    result1 = pi1 >> asfreq(args=["3M"])
    result2 = pi1 >> asfreq(args=["M"])
    expected = pd.Series(period_range(freq="M", start="2001-12", end="2001-12"))
    tm.assert_numpy_array_equal(result1.index.asi8, expected.index.asi8)
    tm.assert_numpy_array_equal(result2.index.asi8, expected.index.asi8)

def test_ceil():
    dt = pd.Series(Timestamp("20130101 09:10:11"))
    result = dt >> ceil(args=["D"])
    expected = pd.Series(Timestamp("20130102"))
    tm.assert_series_equal(result, expected)


def test_to_timestamp():
        p = pd.Series(Period("1982", freq="A"))
        start_ts = p >> to_timestamp(how="S")
        aliases = ["s", "StarT", "BEGIn"]
        for a in aliases:
            tm.assert_series_equal(start_ts,p >> to_timestamp(args=["D"], how=a))
            # freq with mult should not affect to the result
            tm.assert_series_equal(start_ts,p >> to_timestamp(args=["3D"], how=a))

        end_ts = p >> to_timestamp(how="E")
        aliases = ["e", "end", "FINIsH"]
        for a in aliases:
            tm.assert_series_equal(end_ts, p >> to_timestamp(args=["D"], how=a))
            tm.assert_series_equal(end_ts, p >> to_timestamp(args=["3D"], how=a))

        from_lst = ["A", "Q", "M", "W", "B", "D", "H", "Min", "S"]
            
        for i, fcode in enumerate(from_lst):
            p = pd.Series(Period("1982", freq=fcode))
            step1 = p >> to_timestamp()
            result = step1.dt.to_period(fcode)
            tm.assert_series_equal(result, p)

            tm.assert_series_equal(p.dt.start_time, p >> to_timestamp(how="S"))

        # Frequency other than daily
        p = pd.Series(Period("1985", freq="A"))

        result = p >> to_timestamp(args=["H"], how="end")
        expected = pd.Series(Timestamp(1986, 1, 1) - Timedelta(1, "ns"))
        tm.assert_series_equal(result, expected)
        result = p >> to_timestamp(args=["3H"], how="end")
        tm.assert_series_equal(result, expected)

        result = p >> to_timestamp(args=["T"], how="end")
        expected = pd.Series(Timestamp(1986, 1, 1) - Timedelta(1, "ns"))
        tm.assert_series_equal(result, expected)
        result = p >> to_timestamp(args=["2T"], how="end")
        tm.assert_series_equal(result, expected)

        result = p >> to_timestamp(how="end")
        expected = pd.Series(Timestamp(1986, 1, 1) - Timedelta(1, "ns"))
        tm.assert_series_equal(result, expected)

        expected = pd.Series(datetime(1985, 1, 1))
        result = p >> to_timestamp(args=["H"], how="start")
        tm.assert_series_equal(result, expected)
        result = p >> to_timestamp(args=["T"], how="start")
        tm.assert_series_equal(result, expected)
        result = p >> to_timestamp(args=["S"], how="start")
        tm.assert_series_equal(result, expected)
        result = p >> to_timestamp(args=["3H"], how="start")
        tm.assert_series_equal(result, expected)
        result = p >> to_timestamp(args=["5S"], how="start")
        tm.assert_series_equal(result, expected)


@pytest.fixture
def timedelta_index():
    """
    A fixture to provide TimedeltaIndex objects with different frequencies.
     Most TimedeltaArray behavior is already tested in TimedeltaIndex tests,
    so here we just test that the TimedeltaArray behavior matches
    the TimedeltaIndex behavior.
    """
    # TODO: flesh this out
    return TimedeltaIndex(["1 Day", "3 Hours", "NaT"])
def test_total_seconds(timedelta_index):
        tdi = pd.Series(timedelta_index)
        arr = pd.Series(TimedeltaArray(tdi))

        expected = tdi >> total_seconds()
        result = arr >> total_seconds()

        tm.assert_series_equal(result, expected)


@pytest.fixture(params=[pd.DataFrame, pd.Series])
def frame_or_series(request):
    """
    Fixture to parametrize over DataFrame and Series.
    """
    return request.param
def test_tz_localize(frame_or_series):
        rng = date_range("1/1/2011", periods=100, freq="H")

        obj = DataFrame({"a": 1}, index=rng)
        if frame_or_series is not DataFrame:
            obj = obj["a"]

        result = obj.tz_localize("utc")
        expected = DataFrame({"a": 1}, pd.Series(rng) >> tz_localize(args=["UTC"]))
        if frame_or_series is not DataFrame:
            expected = expected["a"]

        assert result.index.tz.zone == "UTC"
        tm.assert_equal(result, expected)