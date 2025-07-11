"""
语法基础

- Python      强类型动态语言
- Java        强类型静态语言
- JavaScript  弱类型动态语言
"""
import copy


# region 内置函数：https://docs.python.org/zh-cn/3/library/functions.html
class TestBuiltinFunctions:
    """
    ``_
    """

    def test_print(self):
        print("广州", "深圳", "中山", sep=" ", end="\n")

    def test_id(self):
        """id()：返回对象内存地址"""
        id(1)

    def test_iter_next(self):
        """
        - iter()：返回一个 iterator 对象
        - next()：通过调用 iterator 的 __next__() 方法获取下一个元素
        """
        iterator = iter(range(1, 3))
        assert next(iterator) == 1
        assert next(iterator) == 2

    def test_range_sum(self):
        result = 0
        r = range(1, 101, 1)
        for i in r:
            result += i
        assert result == sum(r)

    def test_type_conversion(self):
        """类型转换：int(), float(), chr(), str(), tuple(), list(), eval()"""
        assert int(1.8) == 1
        assert list('hello') == ['h', 'e', 'l', 'l', 'o']
        assert list({'name': 'ljh', 'age': 18}) == ['name', 'age']
        assert eval('1+1') == 2
        assert type(eval('[1, 2, 3]')) == list

    def test_eval_exec(self):
        """
        eval() 对比 exec()

        - 功能：计算表达式的值；执行任意代码块
        - 返回值：返回表达式结果；总是返回 None
        - 语法支持：仅表达式（无复制、循环等）；完整 Python 语法
        """
        pass


# endregion
# region 内置类型：https://docs.python.org/zh-cn/3/library/stdtypes.html
def test_builtin_types():
    """
    1. 不可变类型：修改操作实际创建新对象，内存地址改变，可用作字典键
        1. 数值：int, flot, complex, bool
        2. 文本序列：str
        3. 序列：tuple，range
        4. 二进制序列：bytes
        5. 集合：frozenset

    2. 可变类型：支持原地修改，不可用作字典键
        1. 序列：list
        2. 二进制序列：bytearray
        3. 映射：dict
        4. 集合：set
    """
    # bool 是 int 子类，False 和 True 的行为分别与整数 0 和 1 类似，但是不建议这样使用
    assert True + False == 1
    # 字符串方法
    # find() 未找到到返回 -1，index() 未找到引发 ValueError
    assert "watermelon".find("melon") == "watermelon".index("melon")
    assert "banana".count("a") == 3
    assert "blood".replace("o", "e") == "bleed"
    # encode(), decode()
    h_encode = "hello".encode("utf8")
    assert h_encode == b'hello'
    assert h_encode.decode("utf8") == "hello"


# endregion
# region 内置类型-序列类型：https://docs.python.org/zh-cn/3/library/stdtypes.html#sequence-types-list-tuple-range
# 元组和序列：https://docs.python.org/zh-cn/3/tutorial/datastructures.html#tuples-and-sequences
def test_sequence_types():
    """
    核心特征：
        1. 有序性
        2. 索引访问
        3. 切片操作
        4. 可迭代：for
        5. 长度计算：len(seq)

    `按可变性分类 <https://docs.python.org/zh-cn/3.15/reference/datamodel.html#sequences>`_：
        1. 不可变序列：str tuple range bytes
        2. 可变序列：list bytearray
    """
    # 索引访问
    assert "hello"[-1] == "o"
    assert "water" in "watermelon"
    assert "fire" not in "watermelon"
    assert "a" * 3 == "aaa"
    # 切片
    assert "watermelon"[0:5] == "water"
    assert "watermelon"[-5:] == "melon"
    assert "watermelon"[-1:-3:-1] == "no"
    assert len("hello") == 5
    assert min("hello") == "e"
    assert max("hello") == "o"
    assert "hello".count("l") == 2
    # 添加、扩展、插入
    seq = ['a', 'b', 'c']
    seq.append('d')
    assert seq == ['a', 'b', 'c', 'd']
    seq.extend('eg')
    assert seq == ['a', 'b', 'c', 'd', 'e', 'g']
    seq.insert(5, 'f')
    assert seq == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    seq.pop()
    seq.pop(len(seq) - 1)
    assert seq == ['a', 'b', 'c', 'd', 'e']
    seq.remove('e')
    assert seq == ['a', 'b', 'c', 'd']
    # 列表推导式
    assert [global_x * 2 for global_x in range(1, 10) if global_x <= 3] == [2, 4, 6]
    # 元组只有一个元素时，type()返回元素的类型，而不是元组类型
    assert type((1)) == int
    assert type((1,)) == tuple


# endregion
# region 内置类型-集合类型：https://docs.python.org/zh-cn/3/library/stdtypes.html#set-types-set-frozenset
def test_set_types():
    """
    不同可哈希对象的无序集合

    两种内置 Set：
        1. set：可变的，所以没有哈希值；不能被用作字典的键或其他 set 的元素
        2. frozenset：不可变且可哈希；可以被用作字典的键或其他 set 的元素
        """
    # 空 Set
    s = set()
    s.add('a')
    # 更新集合，添加来自 others 中的所有元素
    s.update(['b', 'c', 'd', 'e'])
    s.remove('e')
    assert s == {'d', 'c', 'b', 'a'}
    # 存在则移除
    s.discard('f')
    assert s == {'d', 'c', 'b', 'a'}
    # 移除并返回左一元素
    # 由于 int 哈希值等于其本身，所以此 set ‘实现了有序’，左一元素永远是1
    assert {1, 2, 3}.pop() == 1
    # 交集
    assert {1, 2} & {3, 4} == set()
    assert {1, 2}.intersection({3, 4}) == set()
    # 并集
    assert {1, 2} | {2, 3} == {1, 2, 3}
    assert {1, 2}.union({2, 3}) == {1, 2, 3}
    # 差集
    assert {1, 2} - {2, 3} == {1}
    assert {1, 2}.difference({2, 3}) == {1}
    # 对称差集
    assert {1, 2} ^ {2, 3} == {1, 3}
    assert {1, 2}.symmetric_difference({2, 3}) == {1, 3}
    # 交集是否为 null
    assert {1, 2}.isdisjoint({3, 4})
    # 是否为子集
    assert {1, 2}.issubset({1, 2, 3})
    # 是否为超集
    assert {1, 2, 3}.issuperset({1, 2})


# endregion
# region 内置类型-映射类型：https://docs.python.org/zh-cn/3/library/stdtypes.html#mapping-types-dict
def test_mapping_types():
    d = {'name': 'ljh', 'age': 18}
    assert type(d) == dict
    assert len(d) == 2
    # keys()、values()、items() 返回的对象是试图对象
    assert type(d.keys()).__name__ == 'dict_keys'
    assert type(d.values()).__name__ == 'dict_values'
    assert type(d.items()).__name__ == 'dict_items'
    d.pop('age')
    d['age'] = 123
    assert d.popitem() == ('age', 123)
    d.clear()
    assert d == {}
    # 字典推导式
    assert {global_x: global_x ** 2 for global_x in range(1, 10) if global_x <= 3} == {1: 1, 2: 4, 3: 9}


# endregion
# region 数据类型-copy：https://docs.python.org/zh-cn/3/library/copy.html
def test_copy():
    c = [1, 2, [3, 4]]
    c2 = c
    assert id(c) == id(c2)
    # 浅拷贝
    c3 = copy.copy(c)
    assert id(c) != id(c3)
    assert id(c[2]) == id(c3[2])
    # 深拷贝
    c4 = copy.deepcopy(c)
    assert id(c) != id(c4)
    assert id(c[2]) != id(c4[2])


# endregion
# region 表达式：https://docs.python.org/zh-cn/3/reference/expressions.html
# 运算符：https://docs.python.org/zh-cn/3/reference/lexical_analysis.html#operators
def test_expressions():
    # 除法结果是 float
    assert type(6 / 2) == float
    # 整除
    assert 7.0 // 2 == 3
    assert type(7 // 2) == int
    assert type(7.0 // 2) == float
    # 幂运算
    assert 2 ** 3 == 8


# endregion 运算
# region 简单语句：https://docs.python.org/zh-cn/3/reference/simple_stmts.html
global_x, global_y, global_z = (0, 0, 0)


class TestSimpleStatements:
    def test_del_statement(self):
        """
        del 语句
    
        1. 与赋值相似，时递归定义的
        2. 删除列表会从左到右删除每个目标
        3. 属性引用、抽取和切片的删除会被传递给相应的原型对象
        """
        # 递归删除切片
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        del matrix[1:3]
        del matrix[0][1:]
        assert matrix == [[1]]

    def test_return_statement(self):
        """
        return 语句

        1. return 离开当前函数调用，并以表达式列表（或 None）作为返回值
            a. 没有返回值时，返回 None
            b. 多个返回值时，返回元组
        2. 生成器函数
            a. 普通生成器函数：允许 return value；完成信号引发 StopIteration，返回值存储在 StopIteration.value
            b. 异步生成器函数：只允许 return （无值）；完成信号引发 StopAsyncIteration
        """

        def number_generator(n):
            for i in range(1, n):
                yield i + 1
            return f"生成第 {n} 个数字"

        gen = number_generator(3)
        try:
            while True: next(gen)
        except StopIteration as e:
            print(f"捕获 StopIteration: {e.value}")

    def test_global_statement(self):
        """
        global 语句

        1. 使标识符被解释为全局变量
        2. 给全局变量赋值，必须使用 global
        3. global 语句只在当前编译单元有效
            a. 每个模块（.py 文件）
            b. 每个交互式命令
            c. 每个传递给 exec/eval/compile 的参数
        """
        global global_x, global_y, global_z

        def modify_globals():
            global global_x
            global_x = 1
            global_y = 1

            exec_code = """
global global_z
global_z = 1
"""
            exec(exec_code, {})

        modify_globals()
        assert global_x == 1
        assert global_y == 0
        assert global_z == 0

    def test_nonlocal_statement(self):
        """
        nonlocal 语句

        1. 使标识符引用先前在非局部作用域中绑定的名称
        2. 如果名称在多个非局部作用域中绑定，则使用最近的一个绑定
        3. nonlocal 语句只在当前编译单元有效，同 global
        """
        nonlocal_x = 0

        def outer():
            nonlocal_x = 1

            def inner():
                nonlocal nonlocal_x
                nonlocal_x = 2
                print('inner x:', nonlocal_x)

            inner()
            print('outer x:', nonlocal_x)

        outer()
        print('x:', nonlocal_x)


# endregion
# region 控制流程工具-定义函数
class TestDefiningFunctions:
    """
    1. `简介 <https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions>`_
    2. `更多 <https://docs.python.org/zh-cn/3/tutorial/controlflow.html#more-on-defining-functions>`_
    """

    def test_arguments(self):
        def func1(po1s, pos2=0, /, pk1=0, pk2=0, *, kwd1, kwd2):
            """
            1. 仅限位置参数：在 / 前
            2. 仅限关键字参数：在 * 后
            3. 在 / 和 * 之间，或未使用 / 和 * 时，参数可以按位置或关键字传递给函数
            4. 关键字参数必须跟在位置参数后面
            5. 关键字参数顺序并不重要
            6. 如果一个形参具有默认值，后续所有在 "*" 之前的形参也必须具有默认值
            """
            pass

        func1(1, 2, 3, 4, kwd1=5, kwd2=6)
        func1(1, 2, 3, pk2=4, kwd1=5, kwd2=6)
        func1(1, 2, kwd2=6, kwd1=5, pk2=4, pk1=3)

    def func2(self, kind, *pos, **kwd):
        """
        :param kind:
        :param pos: 接受一个元组，包含形参列表之外的位置参数；该形参后只能是仅限关键字参数
        :param kwd: 接受一个字典，包含形参列表之外的关键字参数
        """
        pass

    def test_arbitrary_argument_lists(self):
        """
        `任意参数列表 <https://docs.python.org/zh-cn/3/tutorial/controlflow.html#arbitrary-argument-lists>`_
        """

        self.func2(1, 2, 3, 4, kwd1=5, kwd2=6)

    def test_unpacking_argument_lists(self):
        """
        `解包实参列表 <https://docs.python.org/zh-cn/3/tutorial/controlflow.html#unpacking-argument-lists>`_
        """
        r = range(2, 5)
        d = {"kwd1": 5, "kwd2": 6}
        self.func2(1, *r, **d)

    def test_lamda_expressions(self):
        """
        `Lambda 表达式 <https://docs.python.org/zh-cn/3/tutorial/controlflow.html#lambda-expressions>`_
        """
        add = lambda a, b=0: a + b
        assert add(1, 1) == 2
        assert add(1) == 1
        # lambda 作为参数
        pairs = [(4, 'four'), (2, 'two'), (1, 'one'), (3, 'three')]
        pairs.sort(key=lambda pair: pair[0])
        assert pairs == [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]


# endregion
# region 输入与输出-格式化字符串
# 更复杂的输出格式：https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#fancier-output-formatting
def test_string_formatting():
    year = 2025
    month = 7
    day = 2
    assert "Today is %d-%02d-%02d" % (year, month, day) == "Today is 2025-07-02"
    assert f"Today is {year}-{month:02d}-{day:02d}" == "Today is 2025-07-02"

# endregion
