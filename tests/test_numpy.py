import numpy as np

from src.utils.timer import Timer


# region NumPy 模块结构：https://numpy.org/doc/stable/reference/module_structure.html
class TestNumPysModuleStructure:
    def test_string_functionality(self):
        """
        `字符串功能 <https://numpy.org/doc/stable/reference/routines.strings.html>`_
        """
        # center(a, width[, fillchar])          元素居中，并使用指定字符填充至指定宽度
        assert np.array_equal(np.strings.center(['1', '2', '3'], 3, '*'), ['*1*', '*2*', '*3*'])

        # capitalize(a)                         元素首字母大写
        assert np.array_equal(np.strings.capitalize(['cat', 'dog']), ['Cat', 'Dog'])

        # title(a)                              单词首字母大写
        assert np.array_equal(np.strings.title(['i love u']), ['I Love U'])


# endregion

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
                ndarray(shape[, dtype, buffer, offset, strides, order])
                """

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
            # 一维迭代器
            assert np.array_equal(list(arr.flat), [1, 2, 3, 2, 3, 4])

    class TestDataTypePromotion:
        """
        `数据类型提升 <https://numpy.org/doc/stable/reference/arrays.promotion.html>`_：
            一般提升路径：bool → int → float → complex → str / object
        """

    class TestIteratingOverArrays:
        """
        `迭代数组 <https://numpy.org/doc/stable/reference/arrays.nditer.html>`_：

        `numpy.nditer <https://numpy.org/doc/stable/reference/generated/numpy.nditer.html#numpy-nditer>`_：
        """

        class TestSingleArrayIteration:
            """单数组迭代"""
            a = np.arange(6).reshape(2, 3)

            def test_controlling_iteration_order(self):
                """控制迭代顺序"""
                # K (Keep)：默认策略，“怎么存就怎么取”，性能最高
                assert np.array_equal([x for x in np.nditer(self.a.copy(order='C'), order='K')], [0, 1, 2, 3, 4, 5])
                assert np.array_equal([x for x in np.nditer(self.a.copy(order='F'), order='K')], [0, 3, 1, 4, 2, 5])
                # a 和 a.T 都是默认按 C 顺序存储，所以被遍历顺序相同
                assert np.array_equal([x for x in np.nditer(self.a)], [x for x in np.nditer(self.a.T)])

                # C 顺序遍历：行优先，内存顺序
                assert np.array_equal([x for x in np.nditer(self.a, order='C')], [0, 1, 2, 3, 4, 5])

                # Fortran 顺序遍历：列优先
                assert np.array_equal([x for x in np.nditer(self.a, order='F')], [0, 3, 1, 4, 2, 5])

            def test_modifying_array_values(self):
                """
                修改数组值

                1. 默认将输入操作数视为只读对象
                2. 修改数组元素，必须使用每个数的 'readwrite' 或 ’writeonly' 标志
                3. 必须在迭代结束后将缓冲数组复制回到原数组：①with 语句 ②close()
                """
                with np.nditer(self.a, op_flags=['readwrite']) as it:
                    for x in it:
                        x[...] = 2 * x
                assert np.array_equal(self.a, [[0, 2, 4], [6, 8, 10]])

            def test_external_loop_and_buffering(self):
                """
                external_loop

                1. 不使用 external_loop：迭代器每次只返回一个元素
                2. 使用 external_loop：迭代器尽可能多地收集内存连续的元素，打包成一个1维数组返回
                """
                assert np.array_equal(sum(1 for _ in np.nditer(self.a.T)), 6)
                # 内存连续，只需遍历1次
                assert np.array_equal(sum(1 for _ in np.nditer(self.a.T, flags=['external_loop'])), 1)
                # 内存不连续，需要遍历6次
                assert np.array_equal(sum(1 for _ in np.nditer(self.a.T, flags=['external_loop'], order='F')), 6)
                # 启用缓冲，即使内存不连续，也只需遍历1次
                assert np.array_equal(sum(1 for _ in np.nditer(self.a, flags=['external_loop', 'buffered'], order='F')), 1)

            def test_tracking_index_or_multi_index(self):
                """追踪索引或多索引"""
                # c_index：追踪 C 顺序索引
                it = np.nditer(self.a, flags=['c_index'])
                assert np.array_equal([it.index for _ in it], [0, 1, 2, 3, 4, 5])
                # f_index：追踪 Fortran 顺序索引
                it = np.nditer(self.a, flags=['f_index'])
                assert np.array_equal([it.index for _ in it], [0, 2, 4, 1, 3, 5])
                # multi_index：追踪多索引
                it = np.nditer(self.a, flags=['multi_index'])
                assert np.array_equal([it.multi_index for _ in it], [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)])

            def test_alternative_looping(self):
                """替代循环"""
                it = np.nditer(self.a, flags=['f_index'])
                while not it.finished:
                    it.iternext()

        class TestBroadcastingArrayIteration:
            """广播数组迭代"""

            def test(self):
                a = np.arange(3)
                b = np.arange(6).reshape(2, 3)
                assert np.array_equal([(x, y) for x, y in np.nditer([a, b])], [(0, 0), (1, 1), (2, 2), (0, 3), (1, 4), (2, 5)])

            def test_iterator_allocated_output_arrays(self):
                """迭代器分配的输出数组"""

                def square(a):
                    with np.nditer([a, None]) as it:
                        for x, y in it:
                            y[...] = x * x
                        return it.operands[1]

                assert np.array_equal(square([1, 2, 3]), [1, 4, 9])

            def test_outer_product_iteration(self):
                """外积迭代"""
                a = np.arange(2)
                b = np.arange(4).reshape(2, 2)
                # op_axes：显示地控制维度对齐
                # [0, -1, -1] 表示 [a的第0维, 新轴, 新轴], 即 a 形状 (2,) → (2, 1, 1)
                # [-1, 0, 1] 表示 [新轴, b的第0维, b的第1维], 即 b 形状 (2, 2) → (1, 2, 2)
                it = np.nditer([a, b, None], op_axes=[[0, -1, -1], [-1, 0, 1], None])
                with it:
                    for x, y, z in it:
                        z[...] = x * y
                    result = it.operands[2]
                assert np.array_equal(result, [[[0, 0], [0, 0]], [[0, 1], [2, 3]]])


# endregion

# region 按主题分类的例程和对象：https://numpy.org/doc/stable/reference/routines.html
class TestRoutinesAndObjectsByTopic:
    class TestArrayManipulationRoutines:
        """
        `数组操作 <https://numpy.org/doc/stable/reference/routines.array-manipulation.html>`_
        """

        def test_basic_operations(self):
            """基础操作"""
            a = np.array([[1, 2, 3], [2, 3, 4]])
            # 维度的数量
            assert a.ndim == np.ndim(a) == 2
            # 维度的元组
            assert a.shape == np.shape(a) == (2, 3)
            # 指定轴元素的数量
            assert a.size == 2 * 3
            assert np.size(a, 1) == 3

        def test_changing_array_shape(self):
            """改变数组形状"""
            a = np.arange(6)
            # reshape(a, /, shape[, order, copy])   返回一个包含相同数据但具有新形状的数组
            # 内存连续返回视图，不连续返回副本
            reshape_arr = a.reshape(2, 3)
            assert np.array_equal(reshape_arr, np.array([[0, 1, 2],
                                                         [3, 4, 5]]))
            # flatten([order])                      返回一个一维数组副本
            assert np.array_equal(list(reshape_arr.flatten()), [0, 1, 2, 3, 4, 5])
            # ravel(a[, order])                     返回一个一维数组视图
            assert np.array_equal(list(reshape_arr.ravel()), [0, 1, 2, 3, 4, 5])

        def test_transpose_like_operations(self):
            """转置类操作"""
            a = np.arange(8).reshape(2, 2, 2)
            # ndarray.T                     返回转置数组视图
            assert np.array_equal(a.T, [[[0, 4], [2, 6]], [[1, 5], [3, 7]]])
            # transpose(a[, axes])          返回一个轴转置的数组
            assert np.array_equal(np.transpose(a), [[[0, 4], [2, 6]], [[1, 5], [3, 7]]])
            assert np.array_equal(np.transpose(a, (1, 0, 2)), [[[0, 1], [4, 5]], [[2, 3], [6, 7]]])
            assert np.array_equal(np.transpose(a, (0, 2, 1)), [[[0, 2], [1, 3]], [[4, 6], [5, 7]]])
            assert np.array_equal(np.transpose(a, (2, 1, 0)), [[[0, 4], [2, 6]], [[1, 5], [3, 7]]])
            # 对于一维数组不起作用
            b = np.array([0, 1, 2])
            assert np.array_equal(b.T, b)
            # rollaxis(a, axis[, start])    将 axis 轴移到 start 位置
            assert np.array_equal(np.rollaxis(a, 0, 2), [[[0, 1], [4, 5]], [[2, 3], [6, 7]]])
            # swapaxes(a, axis1, axis2)     交换 axis1 和 axis2 轴
            assert np.array_equal(np.swapaxes(a, 0, 2), [[[0, 4], [2, 6]], [[1, 5], [3, 7]]])

        class TestChangingNumberOfDimensions:
            """改变维度数"""

            def test_broadcast(self):
                """
                broadcast(*arrays)：生成一个模仿广播的对象。
                    对输入参数进行广播，并返回一个封装结果的对象。它具有 shape 和 nd 属性，并可用作迭代器。
                """
                x = np.array([[1], [2], [3]])
                y = np.array([4, 5, 6])
                a = np.broadcast(x, y)
                assert a.shape == (3, 3) and a.nd == 2

            def test_broadcast_to(self):
                """
                broadcast_to(array, shape[, subok])：将数组广播到新的形状。返回具有给定形状的原始数组的只读视图。
                """
                x = np.array([0, 1])
                a = np.broadcast_to(x, (2, 2))
                assert np.array_equal(a, [[0, 1], [0, 1]])

            def test_squeeze(self):
                """
                squeeze(a[, axis])：移除长度为一的轴。返回的是原数组的视图。
                """
                x = np.array([[[0], [1], [2]]])
                assert x.shape == (1, 3, 1)
                assert np.squeeze(x).shape == (3,)
                assert np.squeeze(x, axis=0).shape == (3, 1)
                assert np.squeeze(x, axis=2).shape == (1, 3)

                y = np.array([[123]])
                assert np.squeeze(y).shape == ()
                assert np.squeeze(y) == 123

            def test_expand_dims(self):
                """
                expand_dims(a, axis)：扩展数组的形状。返回的是原数组的视图。
                """
                x = np.array([1, 2])
                assert x.shape == (2,)
                assert np.expand_dims(x, axis=0).shape == (1, 2)
                assert np.expand_dims(x, axis=1).shape == (2, 1)
                assert np.expand_dims(x, axis=(0, 1)).shape == (1, 1, 2)

        def test_joining_arrays(self):
            """连接数组"""
            a = np.array([[1, 2], [3, 4]])
            b = np.array([[5, 6], [7, 8]])
            # concatenate(arrays, /[, axis, out, dtype, casting])   沿指定轴连接数组
            assert np.array_equal(np.concatenate((a, b), axis=0), [[1, 2], [3, 4], [5, 6], [7, 8]])
            assert np.array_equal(np.concatenate((a, b), axis=1), [[1, 2, 5, 6], [3, 4, 7, 8]])
            assert np.array_equal(np.concatenate((a, b), axis=None), [1, 2, 3, 4, 5, 6, 7, 8])
            # stack(arrays[, axis, out, dtype, casting])            沿新轴连接数组
            assert np.array_equal(np.stack((a, b), axis=0), [[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
            assert np.array_equal(np.stack((a, b), axis=1), [[[1, 2], [5, 6]], [[3, 4], [7, 8]]])
            # vstack(tup, *[, dtype, casting])                      垂直堆叠数组
            assert np.array_equal(np.vstack((a, b)), [[1, 2], [3, 4], [5, 6], [7, 8]])
            # hstack(tup, *[, dtype, casting])                      水平堆叠数组
            assert np.array_equal(np.hstack((a, b)), [[1, 2, 5, 6], [3, 4, 7, 8]])

        def test_splitting_arrays(self):
            """分割数组"""
            a = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
            # split(ary, indices_or_sections[, axis])   分割数组
            split = np.split(a, 2)
            assert np.array_equal(split[0], [[1, 2, 3, 4]])
            assert np.array_equal(split[1], [[5, 6, 7, 8]])
            # vsplit(ary, indices_or_sections)          垂直分割数组
            vsplit = np.vsplit(a, 2)
            assert np.array_equal(vsplit[0], [[1, 2, 3, 4]])
            assert np.array_equal(vsplit[1], [[5, 6, 7, 8]])
            # hsplit(ary, indices_or_sections)          水平分割数组
            hsplit = np.hsplit(a, 2)
            assert np.array_equal(hsplit[0], [[1, 2], [5, 6]])
            assert np.array_equal(hsplit[1], [[3, 4], [7, 8]])

        def test_tiling_arrays(self):
            """平铺数组"""
            # tile(A, reps)                             根据 reps 在各维度复制数组
            a = np.array([0, 1, 2])
            assert np.array_equal(np.tile(a, 2), [0, 1, 2, 0, 1, 2])
            assert np.array_equal(np.tile(a, (1, 1)), [[0, 1, 2]])
            assert np.array_equal(np.tile(a, (2, 1)), [[0, 1, 2], [0, 1, 2]])

        class TestAddingAndRemovingElements:
            """添加和删除元素"""

            def test_resize(self):
                """
                resize(a, new_shape)：创建一个指定新形状的数组。当尺寸与原数组不一致时，会循环重复或截断原数据
                """
                a = np.array([[1, 2], [3, 4]])
                assert np.array_equal(np.resize(a, (2, 3)), [[1, 2, 3], [4, 1, 2]])
                assert np.array_equal(np.resize(a, (1, 3)), [[1, 2, 3]])

            def test_append(self):
                """
                append(arr, values[, axis])：在末尾添加数值或数组，并返回新数组
                """
                a = np.array([[1, 2], [3, 4]])
                assert np.array_equal(np.append(a, [[5, 6]]), [1, 2, 3, 4, 5, 6])
                assert np.array_equal(np.append(a, [[5, 6]], axis=0), [[1, 2], [3, 4], [5, 6]])
                assert np.array_equal(np.append(a, [[5], [6]], axis=1), [[1, 2, 5], [3, 4, 6]])

            def test_insert(self):
                """
                insert(arr, obj, values, axis=None)：在指定轴的指定位置之前插入数值，并返回新数组
                """
                a = np.array([[1, 2], [3, 4]])
                assert np.array_equal(np.insert(a, 0, 0), [0, 1, 2, 3, 4])
                assert np.array_equal(np.insert(a, 0, 0, axis=0), [[0, 0], [1, 2], [3, 4]])
                assert np.array_equal(np.insert(a, 0, 0, axis=1), [[0, 1, 2], [0, 3, 4]])
                assert np.array_equal(np.insert(a, 0, [0, 2], axis=1), [[0, 1, 2], [2, 3, 4]])
                assert np.array_equal(np.insert(a, [0], [[0], [2]], axis=1), [[0, 1, 2], [2, 3, 4]])

            def test_delete(self):
                """
                delete(arr, obj, axis=None)：删除指定位置的子数组，并返回新数组
                """
                a = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
                assert np.array_equal(np.delete(a, 1, axis=0), [[1, 2, 3, 4]])
                assert np.array_equal(np.delete(a, np.s_[::2], axis=1), [[2, 4], [6, 8]])
                assert np.array_equal(np.delete(a, [1, 3, 5, 7]), [1, 3, 5, 7])

            def test_unique(self):
                """
                unique(ar[, return_index, return_inverse, ...])：去重，默认按升序返回
                """
                a = np.array([[2, 2, 3, 1], [4, 2, 3, 3], [2, 2, 3, 1]])
                assert np.array_equal(np.unique(a), [1, 2, 3, 4])
                assert np.array_equal(np.unique(a, axis=0), [[2, 2, 3, 1], [4, 2, 3, 3]])
                a = np.array([1, 2, 5, 4, 2, 3, 2])
                # return_index：返回去重后数组元素在原数组的索引位置
                v, indices = np.unique(a, return_index=True)
                assert np.array_equal(v, [1, 2, 3, 4, 5])
                assert np.array_equal(indices, [0, 1, 5, 3, 2])
                # return_inverse：返回原数组元组在去重后数组的索引位置
                v, indices = np.unique(a, return_inverse=True)
                assert np.array_equal(indices, [0, 1, 4, 3, 1, 2, 1])
                assert np.array_equal(v[indices], a)
                # return_counts：返回去重后数组元素在原数组的出现次数
                v, counts = np.unique(a, return_counts=True)
                assert np.array_equal(counts, [1, 3, 1, 1, 1])
                assert np.array_equal(np.repeat(v, counts), [1, 2, 2, 2, 3, 4, 5])

    class TestInputAndOutput:
        """
        `输入和输出 <https://numpy.org/doc/stable/reference/routines.io.html>`_
        """

        def test_string_formatting(self):
            """字符串格式化"""
            # 浮点数 → 位置计数法的十进制字符串
            assert np.format_float_positional(np.float32(np.pi)) == '3.1415927'
            # 浮点数 → 科学计数法的十进制字符串
            assert np.format_float_scientific(np.float32(np.pi)) == '3.1415927e+00'

    class TestMathematicalFunctions:
        """
        `数学函数 <https://numpy.org/doc/stable/reference/routines.math.html>`_
        """

        def test_trigonometric_functions(self):
            """三角函数"""
            angles_rad = np.array((0, 30, 45, 60, 90)) * np.pi / 180
            # 正弦函数
            assert np.allclose(np.sin(angles_rad), [0, 0.5, 0.70710678, 0.8660254, 1])
            # 余弦函数
            assert np.allclose(np.cos(angles_rad), [1, 0.8660254, 0.70710678, 0.5, 0])
            # 正切函数
            assert np.allclose(np.tan(np.array((0, 30, 45, 60)) * np.pi / 180), [0, 0.57735027, 1, 1.73205081])

        def test_rounding(self):
            """四舍五入"""
            a = np.array([1.054, 1.055])
            assert np.array_equal(np.round(a, 2), [1.05, 1.06])
            assert np.array_equal(np.floor(a * 100) / 100, [1.05, 1.05])
            assert np.array_equal(np.ceil(a * 100) / 100, [1.06, 1.06])

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

        def test_arithmetic_operations(self):
            """算术运算"""
            a = np.array([[1, 2], [3, 4]])
            b = np.array([1., 2.])
            # 逐元素相加
            r = np.add(a, b)
            assert np.array_equal(r, a + b) and np.array_equal(r, [[2, 4], [4, 6]])
            # 逐元素相减
            r = np.subtract(a, b)
            assert np.array_equal(r, a - b) and np.array_equal(r, [[0, 0], [2, 2]])
            # 逐元素相乘
            r = np.multiply(a, b)
            assert np.array_equal(r, a * b) and np.array_equal(r, [[1, 4], [3, 8]])
            # 逐元素相除
            r = np.divide(a, b)
            assert np.array_equal(r, a / b) and np.array_equal(r, [[1, 1], [3, 2]])
            # 逐元素倒数
            assert np.array_equal(np.reciprocal(b), [1, 0.5])

        def test_extrema_finding(self):
            """极值查找"""
            a = np.array([[3, 5, 9, 1, 7], [2, 10, 8, 4, 6]])
            # 最小值
            assert np.min(a) == 1
            assert np.array_equal(np.min(a, 0), [2, 5, 8, 1, 6])
            assert np.array_equal(np.min(a, 1), [1, 2])
            # 最大值
            assert np.max(a) == 10
            assert np.array_equal(np.max(a, 0), [3, 10, 9, 4, 7])
            assert np.array_equal(np.max(a, 1), [9, 10])
            print()


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
        `广播 <https://numpy.org/doc/stable/user/basics.broadcasting.html>`_：
            形状不同的数组执行算术运算时，在满足某些约束条件下，较小数组的形状会“广播”成与较大数组相兼容的形状，
            从而进行逐元素运算，而无需显式复制数据

        三大广播规则：从尾部维度（最右边）开始向前对比

        1. 维度对齐：如果维度数不同，形状较小的数组会在左边补1，直到维度数相同
        2. 兼容检查与拉伸：维度长度相等，或其中一个是1（可拉伸）
        3. 结果形状：结果形状每个维度上的值是输入数组在该维度上的最大值
        """
        a = np.array([[1, 2, 3], [4, 5, 6]])
        assert a.shape == (2, 3)
        b = np.array([10, 20, 30])
        assert b.shape == (3,)
        # 广播：b的形状，维度对齐 (1, 3)，兼容检查与拉伸 (2, 3)
        # 即 [10, 20, 30] → [[10, 20, 30]] → [[10, 20, 30], [10, 20, 30]]
        assert np.array_equal(a + b, [[11, 22, 33], [14, 25, 36]])

        # 显式复制
        c = np.tile(b, (2, 1))
        assert np.array_equal(a + b, a + c)
# endregion
