from composable_pandas.str import capitalize, get
from datetime import datetime

import numpy as np
import pytest
import pandas as pd

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