import numpy as np


# region 数组对象：https://numpy.org/doc/stable/reference/arrays.html
class TestArrayObjects:
    def test_data_type_objects(self):
        """
        `Data type objects <https://numpy.org/doc/stable/reference/arrays.dtypes.html>`_：数据类型对象
        """
        # 简单数据类型
        dt = np.dtype('<i4')
        assert dt.byteorder == '='
        assert dt.kind == 'i'
        assert dt.itemsize == 4
        assert dt.type is np.int32

        # 结构化数据类型
        # [(field_name, field_dtype, field_shape), ...]
        dt = np.dtype([("name", "S20"), ("grades", "i4", (2,)), ("marks", "f4", (3, 4))])
        assert dt.byteorder == '|'
        assert dt.kind == 'V'
        assert dt.itemsize == (20 + 4 * 2 + 4 * 3 * 4)
        assert dt.type is np.void
        dt2 = np.dtype({'names': ['name', 'grades', 'marks'], 'formats': ['S20', ('i4', 2), ('f4', (3, 4))]})
        assert dt == dt2

        # 结构化数据类型（简写，逗号分隔的基本格式字符串）
        # 生成的字段名称：f0, f1, f2, ...
        dt3 = np.dtype("S20, 2i4, (3,4)f4")
        print(dt['name'])
        assert dt3['f0'] == 'S20'
        assert dt3['f1'] == ('<i4', (2,))
        assert dt3['f2'] == ('<f4', (3, 4))

        # (base_dtype, new_dtype)
        # ……

    def test_ndarray(self):
        """
        `The N-dimensional array <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_：N 维数组，元素类型相同
        """
# endregion
