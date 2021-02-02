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
    # GH 6383
    s = Series(
        np.array(
            [
                43,
                48,
                60,
                48,
                50,
                51,
                50,
                45,
                57,
                48,
                56,
                45,
                51,
                39,
                55,
                43,
                54,
                52,
                51,
                54,
            ]
        )
    )

    result = s>>get(25, 0)
    expected = 0
    assert result == expected

    s = Series(
        np.array(
            [
                43,
                48,
                60,
                48,
                50,
                51,
                50,
                45,
                57,
                48,
                56,
                45,
                51,
                39,
                55,
                43,
                54,
                52,
                51,
                54,
            ]
        ),
        index=pd.Float64Index(
            [
                25.0,
                36.0,
                49.0,
                64.0,
                81.0,
                100.0,
                121.0,
                144.0,
                169.0,
                196.0,
                1225.0,
                1296.0,
                1369.0,
                1444.0,
                1521.0,
                1600.0,
                1681.0,
                1764.0,
                1849.0,
                1936.0,
            ]
        ),
    )

    result = s>>get(25, 0)
    expected = 43
    assert result == expected

    # GH 7407
    # with a boolean accessor
    df = pd.DataFrame({"i": [0] * 3, "b": [False] * 3})
    vc = df.i.value_counts()
    result = vc>>get(99, default="Missing")
    assert result == "Missing"

    vc = df.b.value_counts()
    result = vc>>get(False, default="Missing")
    assert result == 3

    result = vc>>get(True, default="Missing")
    assert result == "Missing"