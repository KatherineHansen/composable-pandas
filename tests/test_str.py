
from composable_pandas.str import capitalize, find

from composable_pandas.str import capitalize, findall

from composable_pandas.str import capitalize, get


from composable_pandas.str import capitalize, get_dummies

from datetime import datetime

import numpy as np
import pytest
import pandas as pd

from pandas import DataFrame, Index, MultiIndex, Series, isna, notna
from pandas import Series, _testing as tm

def test_capitalize():
    values = Series(["FOO", "BAR", np.nan, "Blah", "blurg"])
    result = values >> capitalize()
    exp = Series(["Foo", "Bar", np.nan, "Blah", "Blurg"])
    tm.assert_series_equal(result, exp)

    # mixed
    mixed = Series(["FOO", np.nan, "bar", True, datetime.today(), "blah", None, 1, 2.0])
    mixed = mixed >> capitalize()
    exp = Series(["Foo", np.nan, "Bar", np.nan, np.nan, "Blah", np.nan, np.nan, np.nan])
    tm.assert_almost_equal(mixed, exp)



def test_find():
    values = Series(["ABCDEFG", "BCDEFEF", "DEFGHIJEF", "EFGHEF", "XXXX"])
    result = values >> find("EF")
    tm.assert_series_equal(result, Series([4, 3, 1, 0, -1]))
    expected = np.array([v.find("EF") for v in values.values], dtype=np.int64)
    tm.assert_numpy_array_equal(result.values, expected)

    result = values.str.rfind("EF")
    tm.assert_series_equal(result, Series([4, 5, 7, 4, -1]))
    expected = np.array([v.rfind("EF") for v in values.values], dtype=np.int64)
    tm.assert_numpy_array_equal(result.values, expected)

    result = values >> find("EF", start=3)
    tm.assert_series_equal(result, Series([4, 3, 7, 4, -1]))
    expected = np.array([v.find("EF", 3) for v in values.values], dtype=np.int64)
    tm.assert_numpy_array_equal(result.values, expected)

    result = values.str.rfind("EF", 3)
    tm.assert_series_equal(result, Series([4, 5, 7, 4, -1]))
    expected = np.array([v.rfind("EF", 3) for v in values.values], dtype=np.int64)
    tm.assert_numpy_array_equal(result.values, expected)

    result = values >> find("EF", start=3, end=6)
    tm.assert_series_equal(result, Series([4, 3, -1, 4, -1]))
    expected = np.array([v.find("EF", 3, 6) for v in values.values], dtype=np.int64)
    tm.assert_numpy_array_equal(result.values, expected)

    result = values.str.rfind("EF", start=3, end=6)
    tm.assert_series_equal(result, Series([4, 3, -1, 4, -1]))
    expected = np.array([v.rfind("EF", 3, 6) for v in values.values], dtype=np.int64)
    tm.assert_numpy_array_equal(result.values, expected)

    with pytest.raises(TypeError, match="expected a string object, not int"):
        result = values >> find(0)

    with pytest.raises(TypeError, match="expected a string object, not int"):
        result = values.str.rfind(0)

def test_findall():
    values = Series(["fooBAD__barBAD", np.nan, "foo", "BAD"])

    result = values >> findall("BAD[_]*")
    exp = Series([["BAD__", "BAD"], np.nan, [], ["BAD"]])
    tm.assert_almost_equal(result, exp)

    # mixed
    mixed = Series(
        [
            "fooBAD__barBAD",
            np.nan,
            "foo",
            True,
            datetime.today(),
            "BAD",
            None,
            1,
            2.0,
        ]
    )

    rs = Series(mixed) >> findall("BAD[_]*")
    xp = Series(
        [
            ["BAD__", "BAD"],
            np.nan,
            [],
            np.nan,
            np.nan,
            ["BAD"],
            np.nan,
            np.nan,
            np.nan,
        ]
    )

    assert isinstance(rs, Series)
    tm.assert_almost_equal(rs, xp)

def test_get():
    values = Series(["a_b_c", "c_d_e", np.nan, "f_g_h"])

    result = values.str.split("_") >> get(1)
    expected = Series(["b", "d", np.nan, "g"])
    tm.assert_series_equal(result, expected)

    # mixed
    mixed = Series(["a_b_c", np.nan, "c_d_e", True, datetime.today(), None, 1, 2.0])

    rs = Series(mixed).str.split("_") >> get(1)
    xp = Series(["b", np.nan, "d", np.nan, np.nan, np.nan, np.nan, np.nan])

    assert isinstance(rs, Series)
    tm.assert_almost_equal(rs, xp)

    # bounds testing
    values = Series(["1_2_3_4_5", "6_7_8_9_10", "11_12"])

    # positive index
    result = values.str.split("_") >> get(2)
    expected = Series(["3", "8", np.nan])
    tm.assert_series_equal(result, expected)

    # negative index
    result = values.str.split("_") >> get(-3)
    expected = Series(["3", "8", np.nan])
    tm.assert_series_equal(result, expected)


def test_get_dummies():
    s = Series(["a|b", "a|c", np.nan])
    result = s >> get_dummies(sep="|")
    expected = DataFrame([[1, 1, 0], [1, 0, 1], [0, 0, 0]], columns=list("abc"))
    tm.assert_frame_equal(result, expected)

    s = Series(["a;b", "a", 7])
    result = s >> get_dummies(sep=";")
    expected = DataFrame([[0, 1, 1], [0, 1, 0], [1, 0, 0]], columns=list("7ab"))
    tm.assert_frame_equal(result, expected)

    # GH9980, GH8028
    idx = Index(["a|b", "a|c", "b|c"])
    result = idx >> get_dummies(sep="|")

    expected = MultiIndex.from_tuples(
        [(1, 1, 0), (1, 0, 1), (0, 1, 1)], names=("a", "b", "c")
    )
    tm.assert_index_equal(result, expected)

