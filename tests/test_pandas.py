# Series → DataFrame → Panel

import numpy as np
import pandas as pd
from pandas._testing import assert_series_equal as ase, assert_frame_equal as afe


class TestDataStructures:
    """
    `tenacity <https://pandas.pydata.org/docs/user_guide/dsintro.html>`_：多用途重试库
    """

    class TestSeries:
        def test_data(self):
            """
            Series：一个能够容纳任何数据类型（整数、字符串、浮点数、Python 对象等）的一维带标签数组。
                轴标签统称为索引

            s = pd.Series(data, index=index)
            """
            # data 是 ndarry
            a = [1, 2, 3, 4, 5]
            s = pd.Series(np.array(a), index=['a', 'b', 'c', 'd', 'e'])
            assert s.array == a

            # data 是 dict
            d = {"b": 1, "a": 0, "c": 2}
            s = pd.Series(d)
            # 没有指定索引时，键作为索引
            assert list(s.index) == ["b", "a", "c"]
            # 标签对齐
            # 指定索引时，顺序按索引顺序，缺失键对应 nan，多余键丢弃
            i = ["b", "d", "a"]
            s = pd.Series(d, index=i)
            expected = pd.Series([1, np.nan, 0], index=i)
            ase(s, expected)

            # data 是 scalar value
            i = ['a', 'b', 'c', 'd', 'e']
            s = pd.Series(5, index=i)
            expected = pd.Series([5, 5, 5, 5, 5], index=i)
            ase(s, expected)

        s = pd.Series({"a": 5, "b": 4, "c": 3, "d": 2, "e": 1})

        def test_ndarray_like(self):
            s = self.s
            # 位置索引
            assert s.iloc[0] == 5
            # 位置切片
            ase(s.iloc[1:3], pd.Series([4, 3], index=['b', 'c']))
            # 布尔索引
            ase(s[s < s.median()], pd.Series([2, 1], index=['d', 'e']))
            # 按指定索引顺序提取元素
            ase(s.take([3, 1, 2]), pd.Series([2, 4, 3], index=['d', 'b', 'c']))
            # to_numpy()
            np.array_equal(s.to_numpy(), np.array([5, 4, 3, 2, 1]))

        def test_dict_like(self):
            s = self.s
            # 标签索引
            assert s['a'] == 5
            # 标签切片，左闭右闭
            ase(s['b':'c'], s.iloc[1:3])
            assert 'c' in s.index and 'f' not in s.index
            assert s.get('c') == 3 and s.get('f') is None and s.get('f', np.nan) is np.nan

        def test_vectorized_operations(self):
            s = self.s
            """向量化操作"""
            ase(s + s, s * 2)

        def test_attributes_methods(self):
            """
            `Series <https://pandas.pydata.org/docs/reference/api/pandas.Series.html>`_
            """
            s = self.s
            assert s.axes[0].to_list() == ['a', 'b', 'c', 'd', 'e']  # type: ignore[union-attr]
            assert s.dtype == np.int64
            assert s.empty == False
            assert s.ndim == 1
            assert s.size == 5
            np.array_equal(s.values, np.array([5, 4, 3, 2, 1]))
            # head() 和 tail() 默认 5 个
            ase(s.head(), s.tail())

        def test_str(self):
            s = pd.Series(['Mark', 'Lucy', 'John', np.nan, '1234'])
            ase(s.str.len(), pd.Series([4, 4, 4, np.nan, 4]))
            ase(s.str.lower(), pd.Series(['mark', 'lucy', 'john', np.nan, '1234']))
            assert s.iloc[0:2].str.cat(sep='_') == 'Mark_Lucy'
            expected = pd.DataFrame({
                '1234': [0, 0, 0, 0, 1],
                'John': [0, 0, 1, 0, 0],
                'Lucy': [0, 1, 0, 0, 0],
                'Mark': [1, 0, 0, 0, 0]
            })
            afe(s.str.get_dummies(), expected)

    class TestDataFrame:
        """
        DataFrame：一个具有不同类型列的二维标记数据结构
        """
        def test_data(self):
            """
            1. From dict of Series or dicts
            2. From dict of ndarrays / lists
            3. From structured or record array
            4. From a list of dicts
            5. From a Series
            6. From a list of namedtuples
            7. From a list of dataclasses
            8. Alternate constructors
            """
            d = {
                "one": pd.Series([1.0, 2.0, 3.0], index=["a", "b", "c"]),
                "two": pd.Series([1.0, 2.0, 3.0, 4.0], index=["a", "b", "c", "d"]),
            }
            df = pd.DataFrame(d, index=["d", "b", "a"], columns=["two", "three"])
            expected = pd.DataFrame({
                "two": [4.0, 2.0, 1.0],
                "three": [np.nan, np.nan, np.nan]
            }, index=["d", "b", "a"])
            afe(df, expected)
