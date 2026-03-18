import numpy as np


# region 数组对象：https://numpy.org/doc/stable/reference/arrays.html
class TestArrayObjects:
    def test_built_in_scalar_types(self):
        """
        `内置标量类型 <https://numpy.org/doc/stable/reference/arrays.scalars.html#built-in-scalar-types>`_
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
        `数据类型对象 <https://numpy.org/doc/stable/reference/arrays.dtypes.html>`_：

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

    class TestNdarray:
        """
        `N 维数组 <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_：
            一个多维容器，其中包含相同的类型和大小的项目
        """

        class TestConstructingArrays:
            """ 构建数组 """

            class TestArrayCreationRoutines:
                """
                `数组创建例程 <https://numpy.org/doc/stable/reference/routines.array-creation.html#routines-array-creation>`_：
                """
                def test_from_existing_data(self):
                    original = np.array([1, 2, 3])

                    # array(object[, dtype, copy, order, subok, ndmin, ...])
                    # 输入已是 ndarray 时，创建新的副本
                    assert np.array(original) is not original

                    # asarray(a[, dtype, order, device, copy, like])
                    # 输入已是 ndarray 时，直接返回原对象
                    assert np.asarray(original) is original

                    # frombuffer(buffer[, dtype, count, offset, like])
                    # 将 buffer 解释为一维数组
                    assert np.array_equal(np.frombuffer(b'banana', dtype='S1'), [b'b', b'a', b'n', b'a', b'n', b'a'])

                    # fromiter(iter, dtype[, count, like])
                    # 从 iterable 中创建一维数组
                    assert np.array_equal(np.fromiter([1, 2, 3], dtype=int), [1, 2, 3])

                def test_from_shape_or_value(self):
                    # empty(shape[, dtype, order, device, like])
                    # 返回一个给定形状和类型的新数组，不初始化条目
                    assert not np.array_equal(np.empty((2, 2)), np.empty((2, 2)))

                    # zeros(shape[, dtype, order, device, like])
                    # 返回一个给定形状和类型的新数组，填充0
                    assert np.array_equal(np.zeros((2, 2), dtype=int), [[0, 0], [0, 0]])

                    # ones(shape[, dtype, order, device, like])
                    # 返回一个给定形状和类型的新数组，填充1
                    assert np.array_equal(np.ones((2, 2), dtype=int), [[1, 1], [1, 1]])

                    # eye(N[, M, k, dtype, order, device, like])
                    # 返回一个对角线为1，其余位置为0的二维数组
                    assert np.array_equal(np.eye(3, dtype=int), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

                def test_numerical_ranges(self):
                    # arange([start,] stop[, step,][, dtype, ...])
                    assert np.array_equal(np.arange(3), [0, 1, 2])
                    assert np.array_equal(np.arange(0, 3, 1), [0, 1, 2])

                    # linspace(start, stop[, num, endpoint, ...])
                    # 创建等差数列数组
                    assert np.array_equal(np.linspace(1, 9, 5, dtype='i4'), [1, 3, 5, 7, 9])

                    # logspace(start, stop[, num, endpoint, base, ...])
                    # 创建等比数列数组，base 默认为 10
                    assert np.array_equal(np.logspace(1, 3, 3, dtype='i4'), [10, pow(10, 2), pow(10, 3)])

            def test_ndarray_constructor(self):
                """ ndarray(shape[, dtype, buffer, offset, ...]) """

    class TestDataTypePromotion:
        """
        `数据类型提升 <https://numpy.org/doc/stable/reference/arrays.promotion.html>`_：
            一般提升路径：bool → int → float → complex → str / object
        """
# endregion

# region 按主题分类的例程和对象：https://numpy.org/doc/stable/reference/routines.html
class TestRoutinesAndObjectsByTopic:
    class TestRandomSampling:
        """
        `随机抽样 <https://numpy.org/doc/stable/reference/random/index.html>`_
        """

        def test_legacy_generation(self):
            """
            `遗留生成器 <https://numpy.org/doc/stable/reference/random/legacy.html>`_
            """
            # 根据给定形状生成随机浮点数数组，元素范围[0, 1)
            for d3 in np.random.rand(3, 2, 1):
                for d2 in d3:
                    for e in d2:
                        assert 0 <= e < 1

            # randint(low, high=None, size=None, dtype=None)
            # 生成随机整数数组，元素范围[low, high)
            for e in np.random.randint(0, 10, 5):
                assert 0 <= e < 10

            # 根据给定形状生成符合标准正态分布的随机浮点数数组，元素范围(-∞, +∞)
            for e in np.random.randn(10):
                assert -np.inf < e < np.inf

            # normal(loc=0.0, scale=1.0, size=None)
            # 根据给定形状生成任意正态分布的随机浮点数数组，元素范围(-∞, +∞)
            for e in np.random.normal(0, 1, 10):
                assert -np.inf < e < np.inf

# endregion
