import numpy as np

from src.utils.timer import Timer


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
            assert np.dtype(('i', (2, 2))) == '(2,2)int32'
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
            """构建数组"""

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
                """
                ndarray(shape[, dtype, buffer, offset, ...])
                """

        def test_attributes(self):
            """属性"""
            arr = np.array([[1, 2, 3], [2, 3, 4]])
            # 维度数量
            assert arr.ndim == 2
            # 维度元组
            assert arr.shape == (2, 3)
            # 元素数量
            assert arr.size == 2 * 3
            # 元素字节长度
            assert arr.itemsize == arr.dtype.itemsize == 8
            # 内存布局信息
            assert arr.flags.c_contiguous == True
            assert arr.flags.f_contiguous == False
            assert arr.flags.owndata == True
            assert arr.flags.writeable == True
            assert arr.flags.aligned == True
            assert arr.flags.writebackifcopy == False
            # 实部
            assert np.array_equal(arr.real, [[1, 2, 3], [2, 3, 4]])
            # 虚部
            assert np.array_equal(arr.imag, [[0, 0, 0], [0, 0, 0]])

        class TestMethods:
            def test_shape_manipulation(self):
                # reshape(shape)
                assert np.array_equal(np.arange(9).reshape(3, 3), np.array([[0, 1, 2],
                                                                            [3, 4, 5],
                                                                            [6, 7, 8]]))

        def test_internal_memory_layout(self):
            """
            `内部内存布局 <https://numpy.org/doc/stable/reference/arrays.ndarray.html#internal-memory-layout-of-an-ndarray>`_：
                连续的一维计算机内存片段
            """
            import random

            arr = [random.random() for _ in range(1000000)]
            t1, _ = Timer.measure(sum, arr)

            np_arr = np.array(arr)
            t2, _ = Timer.measure(np.sum, np_arr)

            assert t1 > t2 * 3

    class TestDataTypePromotion:
        """
        `数据类型提升 <https://numpy.org/doc/stable/reference/arrays.promotion.html>`_：
            一般提升路径：bool → int → float → complex → str / object
        """


# endregion

# region 按主题分类的例程和对象：https://numpy.org/doc/stable/reference/routines.html
class TestRoutinesAndObjectsByTopic:
    class TestMathematicalFunctions:
        """
        `数学函数 <https://numpy.org/doc/stable/reference/routines.math.html>`_
        """

        def test_sums_products_differences(self):
            # sum(a[, axis, dtype, out, keepdims, ...])
            # 对指定轴上的数组元素求和
            x = np.array([[[0, 1],
                           [2, 3],
                           [4, 5]],
                          [[6, 7],
                           [8, 9],
                           [10, 11]]])
            assert x.sum() == 0 + 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + 11 == 66
            assert np.array_equal(x.sum(0), [[0 + 6, 1 + 7],
                                             [2 + 8, 3 + 9],
                                             [4 + 10, 5 + 11]])
            assert np.array_equal(x.sum(1), [[0 + 2 + 4, 1 + 3 + 5],
                                             [6 + 8 + 10, 7 + 9 + 11]])
            assert np.array_equal(x.sum(2), [[0 + 1, 2 + 3, 4 + 5],
                                             [6 + 7, 8 + 9, 10 + 11]])
            assert np.array_equal(x.sum(axis=(0, 1)), [(0 + 6) + (2 + 8) + (4 + 10), (1 + 7) + (3 + 9) + (5 + 11)])
            assert np.array_equal(x.sum(axis=(1, 2)), [(0 + 2 + 4) + (1 + 3 + 5), (6 + 8 + 10) + (7 + 9 + 11)])
            assert np.array_equal(x.sum(axis=(0, 2)), [(0 + 6) + (1 + 7), (2 + 8) + (3 + 9), (4 + 10) + (5 + 11)])

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

    class TestSortingSearchingAndCounting:

        def test_searching(self):
            # nonzero(a)
            # 返回非零元素的索引
            assert np.array_equal(np.nonzero([True, 0, False, 1])[0], [0, 3])


# endregion

# region NumPy 基础：https://numpy.org/doc/stable/user/basics.html
class TestNumpyFundamentals:
    class TestIndexingOnNdarray:
        """
        `索引 <https://numpy.org/doc/stable/user/basics.indexing.html>`_

        `索引例程 <https://numpy.org/doc/stable/reference/routines.indexing.html>`_
        """

        class TestBasicIndexing:
            """
            `基本索引 <https://numpy.org/doc/stable/user/basics.indexing.html#basic-indexing>`_
            """

            def test_single_element_indexing(self):
                """单元素索引"""
                x = np.array([[0, 1, 2], [3, 4, 5]])
                t1, _ = Timer.measure(lambda arr: [arr[0, 0] for _ in range(10_000)], x)
                t2, _ = Timer.measure(lambda arr: [arr[0][0] for _ in range(10_000)], x)
                # arr[0][0] 第一个索引创建了一个临时数组，所以效率更低
                assert ('耗时：arr[0, 0] < arr[0][0]' ==
                        f'耗时：arr[0, 0] {'<' if t1 < t2 else '=' if t1 == t2 else '>'} arr[0][0]')

            def test_slicing_and_striding(self):
                """
                `切片和步长 <https://numpy.org/doc/stable/user/basics.indexing.html#slicing-and-striding>`_：

                1. 基本切片 将 Python 的切片基本概念扩展到 N 维
                2. 基本切片发生在 obj 是一个：

                    1. slice object (start:stop:step)
                    2. integer
                    3. tuple：contains slice object or integer

                3. 所有通过基本切片生成的数组都是原始数组的视图
                """
                x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
                assert np.array_equal(x[1:7:2], [1, 3, 5])
                assert np.array_equal(x[-3:4:-1], [7, 6, 5])

                x = np.array([[[1], [2], [3]], [[4], [5], [6]]])
                # : 表示全选。因为 start 默认为开头，stop 默认为结尾，step 默认为 1
                assert np.array_equal(x[1:2], x[1:2, :, :])
                assert np.array_equal(x[1:2], [[[4], [5], [6]]])

            def test_dimensional_indexing_tools(self):
                """维度索引工具"""
                x = np.array([[[1], [2], [3]], [[4], [5], [6]]])

                # Ellipsis ...：表示插入足够多的 :（全选）
                assert np.array_equal(x[..., 0], x[:, :, 0])
                assert np.array_equal(x[..., 0], [[1, 2, 3], [4, 5, 6]])

                # np.newaxis (None)：插入一个长度为1的新维度
                assert x.shape == (2, 3, 1)
                assert x[:, np.newaxis, :, :].shape == (2, 1, 3, 1)
                # np.newaxis+广播
                y = np.array([0, 1, 2, 3, 4])
                a = y[:, np.newaxis]
                b = y[np.newaxis, :]
                assert np.array_equal(a, [[0], [1], [2], [3], [4]])
                assert np.array_equal(b, [[0, 1, 2, 3, 4]])
                assert np.array_equal(a + b, [[0, 1, 2, 3, 4],
                                              [1, 2, 3, 4, 5],
                                              [2, 3, 4, 5, 6],
                                              [3, 4, 5, 6, 7],
                                              [4, 5, 6, 7, 8]])

        class TestAdvancedIndexing:
            """
            `高级索引 <https://numpy.org/doc/stable/user/basics.indexing.html#advanced-indexing>`_

            当选择对象是什么对象时，会触发高级索引：

            1. 非元组序列对象
            2. ndarray (integer/bool)
            3. 至少包含一个序列对象或 ndarray (integer/bool) 的元组

            高级索引始终返回数据的副本
            """

            def test_integer_array_indexing(self):
                """整数数组索引"""
                x = np.array([5, 4, 3, 2, 1])
                assert np.array_equal(x[[1, 3, 3, 1]], [4, 2, 2, 4])
                assert np.array_equal(x[np.array([1, 3, 3, 1])], [4, 2, 2, 4])

                # 使用多维索引数组进行索引
                y = np.array([[0, 1, 2, 3, 4],
                              [5, 6, 7, 8, 9],
                              [10, 11, 12, 13, 14],
                              [15, 16, 17, 18, 19],
                              [20, 21, 22, 23, 24]])
                assert np.array_equal(y[[0, 2, 4], [0, 2, 4]], [y[0, 0], y[2, 2], y[4, 4]])
                assert np.array_equal(y[[0, 2, 4], [0, 2, 4]], [0, 12, 24])
                # 广播机制允许索引数组与其他索引的标量结合
                assert np.array_equal(y[[0, 2, 4], 1], [1, 11, 21])

                rows = [[0, 0], [3, 3]]
                columns = [[0, 2], [0, 2]]
                assert np.array_equal(y[rows, columns], [[y[0, 0], y[0, 2]], [y[3, 0], y[3, 2]]])
                assert np.array_equal(y[rows, columns], [[0, 2], [15, 17]])
                # 由于上述索引数组只是重复自身，可以使用广播（比较操作，例如 rows[:, np.newaxis] + columns）来简化
                rows = np.array([0, 3])
                columns = np.array([0, 2])
                assert np.array_equal(rows[:, np.newaxis], [[0], [3]])
                assert np.array_equal(y[rows[:, np.newaxis], columns], [[0, 2], [15, 17]])
                # 这种广播也可以使用 ix_ 函数实现
                assert np.array_equal(y[np.ix_(rows, columns)], [[0, 2], [15, 17]])

            def test_boolean_array_indexing(self):
                """布尔数组索引"""
                x = np.array([[1, 2], [np.nan, 3], [np.nan, np.nan]])
                assert np.array_equal(x[~np.isnan(x)], [1, 2, 3])

                x = np.array([1, -1, -2, 3])
                x[x < 0] += 20
                assert np.array_equal(x, [1, 19, 18, 3])

                x = np.array([[0, 1, 2],
                              [3, 4, 5],
                              [6, 7, 8]])
                y = x > 2
                assert np.array_equal(y, [[False, False, False],
                                          [True, True, True],
                                          [True, True, True]])
                assert np.array_equal(y[:, 2], [False, True, True])
                assert np.array_equal(x[y[:, 2]], [[3, 4, 5],
                                                   [6, 7, 8]])

    def test_broadcasting(self):
        """
        `广播 <https://numpy.org/doc/stable/user/basics.broadcasting.html>`_
        """
        a = np.array([1.0, 2.0, 3.0]) * np.array([2.0, 2.0, 2.0])
        b = np.array([1.0, 2.0, 3.0]) * 2
        assert np.array_equal(a, b)
# endregion
