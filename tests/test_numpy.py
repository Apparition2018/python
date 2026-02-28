import numpy as np


# region 数组对象：https://numpy.org/doc/stable/reference/arrays.html
class TestArrayObjects:
    def test_built_in_scalar_types(self):
        """
        `Built-in scalar types <https://numpy.org/doc/stable/reference/arrays.scalars.html#built-in-scalar-types>`_：内置标量类型
        """
        # generic：numpy 标量类型的基类
        assert np.generic.__mro__ == (np.generic, object)
        print(np.void.__mro__)
        print(np.void.__bases__)

        # 1 number：数值
        assert np.number.__bases__ == (np.generic,)
        # 1.1 integer：精确数值
        assert np.integer.__bases__ == (np.number,)
        # 1.1.1 signedinteger：有符号整数，包括 byte, short, intc, long, int_, intp, longlong, timedelta64
        assert np.signedinteger.__bases__ == (np.integer,)
        assert np.dtype('i1') == 'b' and np.dtype('i2') == 'h' and np.dtype('i4') == 'i' and np.dtype('i8') == 'q'
        assert np.dtype(np.byte).char == 'b' and np.byte is np.int8
        assert np.dtype(np.short).char == 'h' and np.short is np.int16
        assert np.dtype(np.intc).char == 'i'
        assert np.dtype(np.long).char == 'l' and np.long is np.int32
        assert np.dtype(np.int_).char == 'q' and np.int_ is np.int64
        assert np.dtype(np.intp).char == 'q' and np.intp is np.int64
        assert np.dtype(np.longlong).char == 'q' and np.longlong is np.int64
        assert np.dtype(np.timedelta64).char == 'm'
        # 1.1.2 unsignedinteger：无符号整数，包括 ubyte, ushort, uintc, ulong, uint, uintp, ulonglong
        assert np.unsignedinteger.__bases__ == (np.integer,)
        assert np.dtype('u1') == 'B' and np.dtype('u2') == 'H' and np.dtype('u4') == 'L' and np.dtype('u8') == 'Q'
        assert np.dtype(np.ubyte).char == 'B' and np.ubyte is np.uint8
        assert np.dtype(np.ushort).char == 'H' and np.ushort is np.uint16
        assert np.dtype(np.uintc).char == 'I'
        assert np.dtype(np.ulong).char == 'L' and np.ulong is np.uint32
        assert np.dtype(np.uint).char == 'Q' and np.uint is np.uint64
        assert np.dtype(np.uintp).char == 'Q' and np.uintp is np.uint64
        assert np.dtype(np.ulonglong).char == 'Q' and np.ulonglong is np.uint64
        # 1.2 inexact：不精确数值
        assert np.inexact.__bases__ == (np.number,)
        # 1.2.1 floating：浮点数，包括 half, single, double, longdouble
        assert np.floating.__bases__ == (np.inexact,)
        assert (np.dtype('f2') == 'float16' and np.dtype('f2') == 'e'
                and np.dtype('f4') == 'float32' and np.dtype('f4') == 'f'
                and np.dtype('f8') == 'float64' and np.dtype('f8') == 'd')
        assert np.dtype(np.half).char == 'e'
        assert np.dtype(np.single).char == 'f'
        assert np.dtype(np.double).char == 'd'
        assert np.dtype(np.longdouble).char == 'g'
        # 1.2.2 complexfloating：由浮点数组成的复数，包括 csingle, cdouble, clongdouble
        assert np.complexfloating.__bases__ == (np.inexact,)
        assert (np.dtype('c8') == 'complex64' and np.dtype('c8') == 'F'
                and np.dtype('c16') == 'complex128' and np.dtype('c16') == 'D')
        assert np.dtype(np.csingle).char == 'F'
        assert np.dtype(np.cdouble).char == 'D'
        assert np.dtype(np.clongdouble).char == 'G'

        # 2 flexible：没有预定义长度
        assert np.flexible.__bases__ == (np.generic,)
        # 2.1 character：字符字符串
        assert np.character.__bases__ == (np.flexible,)
        # 2.1.1 bytes_：一个字节字符串
        assert np.bytes_.__bases__ == (bytes, np.character)
        assert np.dtype(np.bytes_).char == 'S'
        # 2.1.2 str_：一个 unicode 字符串
        assert np.str_.__bases__ == (str, np.character)
        assert np.dtype(np.str_).char == 'U'
        # 2.2 void
        assert np.character.__bases__ == (np.flexible,)
        assert np.dtype(np.void).char == 'V'

        # 3 bool：布尔类型
        assert np.bool.__bases__ == (np.generic,)
        assert np.dtype(np.bool).char == '?'

        # 4 datetime64
        assert np.datetime64.__bases__ == (np.generic,)
        assert np.datetime64().dtype.char == 'M'

        # 5 object_
        assert np.object_.__bases__ == (np.generic,)
        assert np.dtype(np.object_).char == 'O'

    class TestDataTypeObjects:
        """
        `Data type objects <https://numpy.org/doc/stable/reference/arrays.dtypes.html>`_：
            数据类型对象，描述了以下方面：

        1. 数据的类型
        2. 数据的大小
        3. 字节顺序
        4. 是结构化类型时，每个字段的名称、类型和内存布局
        5. 是子数组时，数组的形状和数据类型

        dtype(dtype[, align, copy])

        1. dtype：必须参数
        2. align：可选布尔值，是否进行内存对齐
        3. copy：可选布尔值，是否复制 dtype 对象
        """
        def test_dtype(self):
            # 1 None：默认 float64
            dt = np.dtype(None)
            assert dt == 'float64'
            # 2 dtype object：原样返回
            assert np.dtype(dt) == dt
            # 3 Array-scalar types
            assert np.dtype(np.int32) == 'int32'
            # 4 Built-in Python types
            assert np.dtype(int) == 'int64'
            # 5 One-character strings
            assert np.dtype('i') == 'int32'
            # 6 Array-protocol type strings
            assert np.dtype('i4') == 'int32'
            # 7 String with comma-separated fields
            # 生成的 field_name 默认为 f0, f1, f2, ...
            dt = np.dtype("S20, 2i4, (3,4)f4")
            assert dt['f0'] == 'S20'
            assert dt['f1'] == ('<i4', (2,))
            assert dt['f2'] == ('<f4', (3, 4))
            # 8 Type strings
            assert np.dtype('int32') == 'int32'
            # 9 (flexible_dtype, itemsize)
            assert np.dtype(('U', 10)) == '<U10'
            # 10 (fixed_dtype, shape)
            assert np.dtype(('i', (2,2))) == '(2,2)int32'
            # 11 [(field_name, field_dtype, field_shape), ...]
            dt = np.dtype([("name", "S20"), ("grades", "i4", (2,)), ("marks", "f4", (3, 4))])
            # 12 {'names': ..., 'formats': ..., 'offsets': ..., 'titles': ..., 'itemsize': ...}
            dt2 = np.dtype({'names': ['name', 'grades', 'marks'], 'formats': ['S20', ('i4', 2), ('f4', (3, 4))]})
            assert dt == dt2
            # 13 (base_dtype, new_dtype)
            base_dtype = np.dtype((np.void, 16))
            new_dtype = np.dtype([('a', 'i8'), ('b', 'i8')])
            arr = np.zeros(3, dtype=(base_dtype, new_dtype))
            arr['a'] = [1, 2, 3]
            arr['b'] = [4, 5, 6]
            assert arr.tolist() == [(1, 4), (2, 5), (3, 6)]

        def test_dtype_copy(self):
            ori_dt = np.dtype(None)
            assert ori_dt is np.dtype(ori_dt, copy=False)
            assert ori_dt is not np.dtype(ori_dt, copy=True)

        def test_checking_data_types(self):
            """
            检查特定数据类型时，使用 == 比较。
            与 Python 类型不同，不应使用 is 进行比较。
            """
            a = np.array([1, 2], dtype=float)
            assert a.dtype == np.dtype(np.float64)
            assert a.dtype == np.float64
            assert a.dtype == float
            assert a.dtype == 'float64'
            assert a.dtype == 'd'

    def test_ndarray(self):
        """
        `The N-dimensional array <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_：N 维数组，元素类型相同
        """
# endregion
