"""
语法基础
- Python      强类型动态语言
- Java        强类型静态语言
- JavaScript  弱类型动态语言
"""
import builtins
from copy import copy, deepcopy
from functools import reduce
from types import FunctionType


# region reStructuredText Docstring Format
class TestReStructuredTextDocstringFormat:
    """
    reStructuredText Docstring Format

    1. `Specification <https://peps.python.org/pep-0287/#specification>`_
    2. `Online editor <https://rsted.info.ucl.ac.be/>`_
    """


# endregion
# region 内置函数：https://docs.python.org/zh-cn/3/library/functions.html
class TestBuiltinFunctions:
    def test_builtin_function(self):
        # id()：返回对象内存地址
        print(id(1))
        # dir()：返回当前本地作用域的名称列表，或指定对象的有效属性列表
        # 不会列出内置函数和变量的名称
        print(dir(builtins))

    def test_print(self):
        print('广州', '深圳', '中山', sep=' ', end='\n')

    def test_range_sum(self):
        result = 0
        r = range(1, 101, 1)
        for i in r:
            result += i
        assert result == sum(r)

    def test_eval_exec(self):
        """
        eval() 对比 exec()

        - 功能：计算表达式的值；执行任意代码块
        - 返回值：返回表达式结果；总是返回 None
        - 语法支持：仅表达式（无复制、循环等）；完整 Python 语法
        """
        assert type(eval('[1, 2, 3]')) == list
        pass

    def test_type_conversion(self):
        """ 类型转换：int(), float(), chr(), str(), tuple(), list(), set() """
        assert int(1.8) == 1
        assert list('hello') == ['h', 'e', 'l', 'l', 'o']
        assert list({'name': 'ljh', 'age': 18}) == ['name', 'age']

    def test_iter_next(self):
        """
        - iter()：返回一个 iterator 对象
        - next()：通过调用 iterator 的 __next__() 方法获取下一个元素
        """
        iterator = iter(range(1, 3))
        assert next(iterator) == 1
        assert next(iterator) == 2

    def test_enumerate_zip(self):
        """
        - enumerate()：返回一个枚举对象
        - zip()：在多个迭代器上并行迭代，从每个迭代器返回一个数据项组成元组
        """
        indexes = [1, 2, 3]
        letters = ['a', 'b', 'c', 'd']
        seasons = ['Spring', 'Summer', 'Fall', 'Winter']
        zip_len = None
        for i, item in enumerate(zip(indexes, letters, seasons)):
            assert item == (indexes[i], letters[i], seasons[i])
            zip_len = i + 1
        # 如果迭代器长度不一样，zip() 按照最短的返回
        assert zip_len == min(len(indexes), len(letters), len(seasons))

    def test_map(self):
        """ map(): 返回一个迭代器，该迭代器将函数应用于可迭代对象的每个项，从而产生结果 """
        assert list(map(lambda x: x * 2, [1, 2, 3])) == [2, 4, 6]

    def test_type(self):
        """
        type()：

        1. 传入一个参数时，返回对象的类型，通常与 object.__class__ 相同
        2. 传入三个参数时，返回一个新的类型对象，本质上是 class 语句的一种动态形式

            1. what 字符串：类名，并会成为 __name__ 属性
            2. base 元组：成为 __base__ 属性，如果为空，则会添加所有类的终极基类 object
            3. dict 字典：属性和方法，成为 __dict 属性
        """
        assert type('a') == 'a'.__class__
        X = type('X', (), dict(a=1))
        assert X.__name__ == 'X'
        assert X.__base__ is object
        assert 'a' in X.__dict__


# endregion
# region 内置类型：https://docs.python.org/zh-cn/3/library/stdtypes.html
class TestBuiltinTypes:
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

    def test_builtin_types(self):
        # bool 是 int 子类，False 和 True 的行为分别与整数 0 和 1 类似，但是不建议这样使用
        assert True + False == 1
        # 字符串方法
        # find() 未找到到返回 -1，index() 未找到引发 ValueError
        assert 'watermelon'.find('melon') == 'watermelon'.index('melon')
        assert 'banana'.count('a') == 3
        assert 'blood'.replace('o', 'e') == 'bleed'
        # encode(), decode()
        h_encode = 'hello'.encode('utf8')
        assert h_encode == b'hello'
        assert h_encode.decode('utf8') == 'hello'

    def test_sequence_types(self):
        """
        `序列类型 <https://docs.python.org/zh-cn/3/library/stdtypes.html#sequence-types-list-tuple-range>`_

        `元组和序列 <https://docs.python.org/zh-cn/3/tutorial/datastructures.html#tuples-and-sequences>`_

        核心特征：

        1. 有序性
        2. 索引访问
        3. 切片操作
        4. 可迭代：for
        5. 长度计算：len(seq)

        `按可变性分类 <https://docs.python.org/zh-cn/3/reference/datamodel.html#sequences>`_：

        1. 不可变序列：str tuple range bytes
        2. 可变序列：list bytearray
        """
        # 索引访问
        assert 'hello'[-1] == 'o'
        assert 'water' in 'watermelon'
        assert 'fire' not in 'watermelon'
        assert 'a' * 3 == 'aaa'
        # 切片
        assert 'watermelon'[0:5] == 'water'
        assert 'watermelon'[-5:] == 'melon'
        assert 'watermelon'[-1:-3:-1] == 'no'
        assert len('hello') == 5
        assert min('hello') == 'e'
        assert max('hello') == 'o'
        assert 'hello'.count('l') == 2
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
        assert [x * 2 for x in range(1, 10) if x <= 3] == [2, 4, 6]
        # 元组只有一个元素时，type()返回元素的类型，而不是元组类型
        assert type((1)) == int
        assert type((1,)) == tuple

    def test_set_types(self):
        """
        `集合类型 <https://docs.python.org/zh-cn/3/library/stdtypes.html#set-types-set-frozenset>`_：
            不重复的可哈希对象的无序集合

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

    def test_mapping_types(self):
        """
        `映射类型 <https://docs.python.org/zh-cn/3/library/stdtypes.html#mapping-types-dict>`_
        """
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
        assert {x: x ** 2 for x in range(1, 10) if x <= 3} == {1: 1, 2: 4, 3: 9}


# endregion
# region 数据类型：https://docs.python.org/zh-cn/3/library/datatypes.html
class TestDataTypes:
    def test_copy(self):
        """
        `copy <https://docs.python.org/zh-cn/3/library/copy.html>`_
        """
        c = [1, 2, [3, 4]]
        c2 = c
        assert id(c) == id(c2)
        # 浅拷贝
        c3 = copy(c)
        assert id(c) != id(c3)
        assert id(c[2]) == id(c3[2])
        #
        c4 = deepcopy(c)
        assert id(c) != id(c4)
        assert id(c[2]) != id(c4[2])


# endregion
# region 函数式编程：https://docs.python.org/zh-cn/3/library/functional.html
class TestFunctional:
    def test_functools(self):
        """
        `functools <https://docs.python.org/zh-cn/3/library/functools.html>`_
        """
        assert reduce(lambda a, b: a + b, [1, 2, 3]) == 6


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
    # 条件表达式/三目运算
    print(1 if True else 0)


# endregion 运算
# region 简单语句：https://docs.python.org/zh-cn/3/reference/simple_stmts.html
class TestSimpleStatements:
    def test_assignment_statements(self):
        # 解包与“加星”目标
        first, *middle, last = [1, 2, 3, 4, 5]
        assert first == 1
        assert middle == [2, 3, 4]
        assert last == 5

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

            1. 没有返回值时，返回 None
            2. 多个返回值时，返回元组

        2. 生成器函数

            1. 普通生成器函数：允许 return value；完成信号引发 StopIteration，返回值存储在 StopIteration.value
            2. 异步生成器函数：只允许 return （无值）；完成信号引发 StopAsyncIteration
        """

        def number_generator(n):
            for i in range(1, n):
                yield i + 1
            return f'生成第 {n} 个数字'

        gen = number_generator(3)
        try:
            while True: next(gen)
        except StopIteration as e:
            print(f'捕获 StopIteration: {e.value}')

    def test_global_nonlocal_statement(self):
        """
        global 语句

        1. 使标识符被解释为全局变量
        2. 给全局变量赋值，必须使用 global
        3. global 语句只在当前编译单元有效

            1. 每个模块（.py 文件）
            2. 每个交互式命令
            3. 每个传递给 exec/eval/compile 的参数

        nonlocal 语句

        1. 使标识符引用先前在非局部作用域中绑定的名称
        2. 如果名称在多个非局部作用域中绑定，则使用最近的一个绑定
        3. nonlocal 语句只在当前编译单元有效，同 global
        """

        def scope_test():
            def do_local():
                spam = 'local spam'

            def do_nonlocal():
                nonlocal spam
                spam = 'nonlocal spam'

            def do_global():
                global spam
                spam = 'global spam'

            spam = 'test spam'
            do_local()
            assert spam == 'test spam'
            do_nonlocal()
            assert spam == 'nonlocal spam'
            do_global()
            assert spam == 'nonlocal spam'

        scope_test()
        assert globals()['spam'] == 'global spam'


# endregion
# region 控制流程工具：https://docs.python.org/zh-cn/3/tutorial/controlflow.html
class TestControlFlowTools:
    class TestDefiningFunctions:
        """
        定义函数

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
                6. 如果一个形参具有默认值，后续所有在 * 之前的形参也必须具有默认值
                """
                return po1s, pos2, pk1, pk2, kwd1, kwd2

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
            d = {'kwd1': 5, 'kwd2': 6}
            self.func2(1, *r, **d)

        def test_pep448(self):
            """
            `PEP 448 - 进一步的解包标准化 <https://docs.python.org/zh-cn/3/whatsnew/3.5.html#whatsnew-pep-448>`_
            """

            def fn(a, b, c, d):
                return a, b, c, d

            assert fn(**{'a': 1, 'c': 3}, **{'b': 2, 'd': 4}) == (1, 2, 3, 4)

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
# region 模块：https://docs.python.org/zh-cn/3/tutorial/modules.html
class TestModules:
    def test__modules(self):
        """
        __name__：获取模块名称

        - 直接运行：__main__
        - 命令行执行：__main__
        - 作为模块导入：模块名
        - 测试框架中：测试文件名

        __all__：__init__.py 的一个可设置变量，设置一个列表，表示 from package import * 要导入的模块
        """
        assert __name__ == 'tests.test_syntax'


# endregion
# region 输入与输出：https://docs.python.org/zh-cn/3/tutorial/inputoutput.html
class TestInputAndOutput:
    def test_string_formatting(self):
        """
        `输出格式化 <https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#fancier-output-formatting>`_
        """
        year = 2025
        month = 7
        day = 2
        # 格式化字符串字面值
        assert f'Today is {year}-{month:02d}-{day:02d}' == 'Today is 2025-07-02'
        # 字符串 format()
        assert 'Today is {year}-{month:02d}-{day:02d}'.format(year=year, month=month, day=day) == 'Today is 2025-07-02'
        # 旧式字符串格式化
        assert 'Today is %d-%02d-%02d' % (year, month, day) == 'Today is 2025-07-02'


# endregion
# region 错误和异常：https://docs.python.org/zh-cn/3/tutorial/errors.html
class TestErrorsAndExceptions:
    def test_handling_exceptions(self):
        """ 异常的处理 """
        try:
            x = int('a')
        except Exception as err:
            print(err)
            assert type(err) == ValueError
            assert err.args[0] == "invalid literal for int() with base 10: 'a'"
            assert err.__str__() == "invalid literal for int() with base 10: 'a'"
        else:
            print(x)
        finally:
            print('Goodbye, world!')

    def test_raising_exceptions(self):
        """ 触发异常 """
        try:
            # 主动触发异常
            raise NameError('HiThere')
        except NameError:
            # 不打算处理异常，重新触发异常
            raise


# endregion
# region 类：https://docs.python.org/zh-cn/3/tutorial/classes.html
class TestClasses:
    pass


# endregion
# region 闭包和装饰器
class TestClosureAndDecorator:
    def test_closure(self):
        """
        闭包：

        1. 嵌套函数
        2. 内部函数引用外部作用域的变量：形成广义闭包
        3. 外部函数返回内部函数：形成“真正”的闭包，支持多次调用保持状态
        """

        def adder(value=0):
            data = {'result': value}

            def inner(increment=1):
                data['result'] += increment
                return data['result']

            return inner

        # 闭包属性
        closure = adder()
        assert hasattr(closure, '__closure__')
        assert closure.__closure__ is not None
        # 自由变量：又称闭包变量，在某个命名空间中被使用的不属于该命名空间中的局部变量的任何变量
        assert closure.__code__.co_freevars == ('data',)
        assert closure.__code__.co_varnames == ('increment',)
        # 访问闭包内容
        cell_contents = closure.__closure__[0].cell_contents if isinstance(closure, FunctionType) else None
        assert cell_contents == {'result': 0}
        # 状态保持能力
        closure()
        assert cell_contents == {'result': 1}
        closure(3)
        assert cell_contents == {'result': 4}
        # 独立实例
        closure2 = adder()
        assert closure2() == 1

    class TestDecorator:
        """
        `装饰器 <https://docs.python.org/zh-cn/3/glossary.html#term-decorator>`_：
            闭包的特例，接受函数作为参数、返回新函数的可调用对象
        """

        def test_method_decorator(self):
            """
            `函数定义 <https://docs.python.org/zh-cn/3/reference/compound_stmts.html#function-definitions>`_
            """

            def log(func):
                def wrapper(*args, **kwargs):
                    print(f'🟢 开始执行: {func.__name__}{args}')
                    result = func(*args, **kwargs)
                    print(f'🔴 执行完成: {func.__name__} -> 返回: {result}')
                    return result

                return wrapper

            def add_tags(tag):
                def decorator(func):
                    def wrapper(*args, **kwargs):
                        result = func(*args, **kwargs)
                        return f'<{tag}>{result}</{tag}>'

                    return wrapper

                return decorator

            @log
            @add_tags('strong')
            @add_tags('div')
            def greet(name):
                return f'Hello, {name}!'

            assert greet('world') == '<strong><div>Hello, world!</div></strong>' != 'Hello, world!'

        def test_class_decorator(self):
            """
            `类定义 <https://docs.python.org/zh-cn/3/reference/compound_stmts.html#class-definitions>`_
            """
            register = []

            def register_class(cls):
                register.append(cls.__name__)
                return cls

            def log(cls):
                old_init = cls.__init__

                def new_init(x, *args, **kwargs):
                    print(f'创建 {cls.__name__} 实例')
                    old_init(x, *args, **kwargs)

                cls.__init__ = new_init
                return cls

            @log
            @register_class
            class DataProcessor: pass

            assert register == ['DataProcessor']
            DataProcessor()

# endregion
