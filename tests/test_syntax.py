"""
语法基础
- Python      强类型动态语言
- Java        强类型静态语言
- JavaScript  弱类型动态语言
"""
import asyncio
import datetime
import inspect
import json
import multiprocessing
import os
import random
import re
import shutil
import tempfile
import threading
import time
from typing import Any

import pytest
from loguru import logger


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
        # callable()：判断对象是否可调用；如果实例所属的类有 __call__() 方法则它就是可调用的
        assert callable(len) is True
        # dir()：返回当前本地作用域的名称列表，或指定对象的有效属性列表
        # 不会列出内置函数和变量的名称
        import builtins
        print(dir(builtins))
        # id()：返回对象内存地址
        print(id(1))
        # round()：将数字四舍五入到给定的精度
        assert round(0.55, 1) == 0.6

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

    def test_repr_str(self):
        """
        repr()：

        1. 目标用户：开发者（调试、日志）
        2. 理想格式：有效的 Python 表达式
        3. 调用方法：__repr__
        4. 调用时机：repr(obj)、交互式解释器中直接输入对象名、容器中显示元素、f-string !r、format() !r、logging %r
        5. 默认行为：返回 <类名 object at 内存地址>
        6. 重建能力：语言规范要求，可被 eval() 重建
        7. 特殊字符：转义

        str()：

        1. 目标用户：用户（显示）
        2. 理想格式：人类可读的描述
        3. 调用方法：__str__
        4. 调用时机：str(obj)、print(obj)、f-string、format()、logging %s
        5. 默认行为：__repr__
        6. 重建能力：无要求
        7. 特殊字符：直接显示
        """

        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

            def __str__(self):
                return f"我是 {self.name}，今年 {self.age} 岁"

            def __repr__(self):
                return f"Person(name='{self.name}', age={self.age})"

            def __eq__(self, other):
                if not isinstance(other, Person):
                    return False
                return self.name == other.name and self.age == other.age

        p = Person("Mary", 18)
        # 容器中显示，输出：[Person(name='Mary', age=18)]
        print([p])
        # 重建对象
        assert eval(repr(p)) == p

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

        # 自定义迭代器
        class Reverse:
            def __init__(self, data):
                self.data = data
                self.index = len(data)

            def __iter__(self):
                return self

            def __next__(self):
                if self.index == 0:
                    raise StopIteration
                self.index = self.index - 1
                return self.data[self.index]

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
        cls_x = type('X', (), dict(a=1))
        assert cls_x.__name__ == 'X'
        assert cls_x.__base__ is object
        assert 'a' in cls_x.__dict__

    def test_function_decorator(self):
        """
        @staticmethod

        1. 将方法转换为静态方法，不会接收隐式的第一个参数
        2. 无法直接访问类属性（只能通过类名），无法访问实例属性
        3. 子类重写父类同名方法是隐藏（Hide）
        4. 使用场景：与类或实例的状态无关，如工具函数

        @classmethod

        1. 将方法转换为类方法，接收类作为隐式的第一个参数 cls
        2. 可通过 cls 访问类属性，无法访问实例属性
        3. 子类重写父类同名方法是覆盖（Override）
        4. 使用场景：

            1. 动态创建类的实例，如替代构造函数
            2. 在继承中保持多态，如工厂方法
            3. 访问或修改类状态，如计数器、配置
        """

        class Parent:
            @staticmethod
            def plus(a, b):
                return a + b

            @classmethod
            def class_name(cls):
                return cls.__name__

        class Child(Parent): pass

        c = Child()
        assert c.plus(1, 2) == 3
        assert c.class_name() == Child.class_name() == Child.__name__
        assert Parent.class_name() == Parent.__name__


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
# region 文本处理服务：https://docs.python.org/zh-cn/3/library/text.html
class TestTextProcessingServices:
    class TestRE:
        """
        `正则表达式操作 <https://docs.python.org/zh-cn/3/library/re.html>`_

        `正则表达式指南 <https://docs.python.org/zh-cn/3/howto/regex.html#regex-howto>`_
        """

        def test_re(self):
            def display_match(match):
                if match is None:
                    return None
                # group() 返回一个或者多个匹配的子组
                # groups 返回一个元组，包含所有匹配的子组
                return '<Match: %r, groups=%r>' % (match.group(), match.groups())

            # r"text" 原始字符串，避免转义问题
            # re.compile() 将正则表达式的样式编译为一个 正则表达式对象
            # 字符串是否为有效扑克牌
            valid = re.compile(r"^[a2-9tjqk]{5}$")
            assert display_match(valid.match("akt5q")) == "<Match: 'akt5q', groups=()>"
            # 字符串是否包含对子
            pair = re.compile(r".*(.).*\1")
            assert display_match(pair.match("717ak")) == "<Match: '717', groups=('7',)>"


# endregion
# region 数据类型：https://docs.python.org/zh-cn/3/library/datatypes.html
class TestDataTypes:
    def test_copy(self):
        """
        `copy <https://docs.python.org/zh-cn/3/library/copy.html>`_
        """
        from copy import copy, deepcopy
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
# region 数字和数学模块：https://docs.python.org/zh-cn/3/library/numeric.html
class TestNumericAndMathematicalModules:
    class TestRandom:
        """
        `生成伪随机数 <https://docs.python.org/zh-cn/3/library/random.html>`_
        """

        def test_random(self):
            # 随机浮点数，0.0 <= x < 1.0
            assert 0 <= random.random() < 1
            # 随机浮点数，1.0 <= x <= 2.0
            assert 1 <= random.uniform(1, 2) <= 2
            # [0, 9] 的整数
            assert random.randint(0, 9) in range(10)
            # [0, 9] 的整数
            assert random.randrange(10) in range(10)
            # [0, 10] 的偶数
            assert random.randrange(0, 11, 2) in range(0, 11, 2)
            # 从非空序列 seq 返回一个随机元素
            assert random.choice(range(10)) in range(10)
            # 洗牌
            l = list(range(10))
            random.shuffle(l)
            print(l)
            # 不重复随机抽样
            print(random.sample(range(10), 3))

        def test_simulations(self):
            # 1. 六次轮盘旋转（可重复的带权重取样）
            # 从 population 中有重复地随机选取元素，返回大小为 k 的元素列表
            print(random.choices(['red', 'black', 'green'], [18, 18, 2], k=6))

            # 2. 从一套扑克 52 张牌中不重复的抽取 20 张，并以十以上的大牌来确定牌的对比值
            # counts=[16, 36] 表示 16 张 high cards，36 张 low cards
            print(random.sample(['high cards', 'low cards'], counts=[16, 36], k=20).count('high cards') / 20)

            # 3. 估计一个被做了手脚的正面朝上概率为 60% 硬币，在 7 次抛掷中得到 5 次及以上正面的概率
            print(sum(random.binomialvariate(n=7, p=0.6) >= 5 for i in range(10_000)) / 10_000)

            # 4. 5 个样本的中位数位于中间两个四分位区之内的概率
            def trial():
                return 2_500 <= sorted(random.choices(range(10_000), k=5))[2] < 7_500

            sum(trial() for i in range(10_000)) / 10_000

        def test_simulate_sampling_from_itertools_combinatoric_iterators(self):
            """
            模拟从 itertools 的排列组合迭代器中进行随机抽样：`例程 <https://docs.python.org/zh-cn/3/library/random.html#recipes>`_
            """


# endregion
# region 函数式编程模块：https://docs.python.org/zh-cn/3/library/functional.html
class TestFunctional:
    def test_functools(self):
        """
        `functools <https://docs.python.org/zh-cn/3/library/functools.html>`_
        """
        from functools import reduce
        assert reduce(lambda a, b: a + b, [1, 2, 3]) == 6


# endregion
# region 文件和目录访问：https://docs.python.org/zh-cn/3/library/filesys.html
class TestFileAndDirectoryAccess:
    def test_pathlib(self):
        """
        `面向对象的文件系统路径 <https://docs.python.org/zh-cn/3/library/pathlib.html>`_
        """
        from pathlib import Path
        p = Path('.')
        print(f"绝对路径：{p.absolute()}")
        print(f"是否存在：{p.exists()}")
        print(f"是否为目录：{p.is_dir()}")
        # 遍历目录下文件
        for _ in p.iterdir(): pass
        # / 操作符可以创建子路径，如 os.path.join()
        p / 'test.txt'

    def test_os_path(self):
        """
        `常用的路径操作 <https://docs.python.org/zh-cn/3/library/os.path.html>`_
        """
        filepath = "./test.txt"
        # 绝对路径
        abs_path = os.path.abspath(filepath)
        assert abs_path == r'D:\Liang\git\python\tests\test.txt'
        dirname = os.path.dirname(abs_path)
        basename = os.path.basename(abs_path)
        print(f"目录：{dirname}")
        print(f"文件名：{basename}")
        print(f"是否为绝对路径：{os.path.isabs(abs_path)}")
        print(f"是否为文件：{os.path.isfile(abs_path)}")
        print(f"是否为目录：{os.path.isdir(abs_path)}")
        print(f"是否为已存在路径：{os.path.exists(abs_path)}")
        print(f"是否指向同一文件：{os.path.samefile(filepath, abs_path)}")
        print(f"文件大小：{os.path.getsize(abs_path)}")
        print(f"创建时间：{time.ctime(os.path.getctime(abs_path))}")
        print(f"最后访问时间：{time.ctime(os.path.getatime(abs_path))}")
        print(f"最后修改时间：{time.ctime(os.path.getmtime(abs_path))}")
        print(f"规范化路径：{os.path.normpath('././test.txt')}")
        # split
        assert os.path.split(abs_path) == (r'D:\Liang\git\python\tests', 'test.txt')
        assert os.path.splitdrive(abs_path) == ('D:', r'\Liang\git\python\tests\test.txt')
        assert os.path.splitroot(abs_path) == ('D:', '\\', r'Liang\git\python\tests\test.txt')
        assert os.path.splitext(abs_path) == (r'D:\Liang\git\python\tests\test', '.txt')
        # join
        assert os.path.join(dirname, basename) == abs_path

    def test_tempfile(self):
        """
        `生成临时文件和目录 <https://docs.python.org/zh-cn/3/library/tempfile.html>`_
        """
        # 创建一个临时文件并向其写入一些数据
        buffer = b'Hello World!'
        with tempfile.TemporaryFile() as fp:
            fp.write(buffer)
            # 从文件读取数据
            fp.seek(0)
            assert fp.read() == buffer
        # delete_on_close：默认 True，文件在 close() 时自动删除
        with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
            fp.close()
            # 文件已被关闭，但因为 delete_on_close=False 所以未被删除
            with open(fp.name, mode='rb') as f:
                f.read()
        # 创建一个临时目录
        with tempfile.TemporaryDirectory() as tmpdir:
            print(tmpdir)

    def test_shutil(self):
        """
        `高层级文件操作 <https://docs.python.org/zh-cn/3/library/shutil.html#module-shutil>`_

        从 Python 3.8 开始，所有涉及文件拷贝的函数 (copyfile(), copy(), copy2(), copytree() 以及 move()) 将会使用平台专属的 "fast-copy" 系统调用以便更高效地拷贝文件
        """
        copy_dir = 'copy'
        # 递归复制目录树，忽略与提供模式匹配的文件和目录
        shutil.copytree('.', copy_dir, ignore=shutil.ignore_patterns('*.py', 'tmp*'))

        # 自定义 ignore 函数，忽略所有目录
        def my_ignore(path, names):
            print(f'Working in {path}')
            return [name for name in names if os.path.isdir(os.path.join(path, name))]

        # dirs_exist_ok，默认 False，是否允许目标目录已存在
        shutil.copytree('.', copy_dir, ignore=my_ignore, dirs_exist_ok=True)
        # 归档（压缩）
        shutil.make_archive('copy', 'zip', copy_dir)
        os.remove('copy.zip')
        # 删除一个完整的目录树
        shutil.rmtree(copy_dir, ignore_errors=True)


# endregion
# region 数据压缩和归档：https://docs.python.org/zh-cn/3/library/archiving.html
class TestDataCompressionAndArchiving:
    def test_zipfile(self):
        """ 操作 ZIP 归档文件 """
        import zipfile
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_zip = f'{tmpdir}/archive.zip'
            # 压缩
            with zipfile.ZipFile(archive_zip, 'w') as z:
                z.write('test.txt')
                z.write('test.json')
            # 解压
            with zipfile.ZipFile(archive_zip, 'r') as z:
                z.extractall(f'{tmpdir}/archive')


# endregion
# region 加密服务：https://docs.python.org/zh-cn/3/library/crypto.html
class TestCryptographicServices:
    def test_hashlib(self):
        """
        `安全哈希和消息摘要 <https://docs.python.org/zh-cn/3/library/hashlib.html>`_
        """
        import hashlib
        data = '123'.encode()
        md1 = hashlib.new('md5', data)
        md2 = hashlib.md5(data)
        assert md1.hexdigest() == md2.hexdigest()
        print(md1.digest())
        print(md1.hexdigest())


# endregion
# region 并发执行：https://docs.python.org/zh-cn/3/library/concurrency.html
class TestConcurrentExecution:
    @staticmethod
    def crawl(link, method):
        logger.info(f"crawl started for {link} by {method}")
        time.sleep(0.01)
        logger.info(f"crawl ended for {link} by {method}")

    links = [
        "https://python.org",
        "https://docs.python.org",
        "https://peps.python.org",
    ]

    def test_concurrency(self):
        from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

        # region：Thread
        threads = []
        for link in self.links:
            t = threading.Thread(target=self.crawl, args=(link,), kwargs={"method": "Thread"})
            threads.append(t)
        for t in threads: t.start()
        for t in threads: t.join()
        # endregion

        # region：Process
        processes = []
        for link in self.links:
            p = multiprocessing.Process(target=self.crawl, args=(link,), kwargs={"method": "Process"})
            processes.append(p)
        for p in processes: p.start()
        for p in processes: p.join()
        # endregion

        # region：ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as executor:
            [executor.submit(self.crawl, link, "ThreadPoolExecutor") for link in self.links]
        # endregion

        # region：ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=3) as executor:
            [executor.submit(self.crawl, link, "ProcessPoolExecutor") for link in self.links]
        # endregion

        # region：Timer：https://docs.python.org/zh-cn/3/library/threading.html#timer-objects
        interval = 0.1
        for link in self.links:
            threading.Timer(interval, self.crawl, args=(link,), kwargs={"method": "Timer"}).start()
        time.sleep(interval * len(self.links))
        # endregion

    class TestThreading:
        """
        `基于线程的并行 <https://docs.python.org/zh-cn/3/library/threading.html>`_：
            提供了一种在单个进程内部并发地运行多个线程的方式；线程适用于 I/O 密集型的任务，如文件操作或发送网络请求

        <a id="gil">全局解释器锁</a>：global interpreter lock，CPython 解释器所采用的一种机制，它确保同一时刻只有一个线程在执行 Python bytecode
        """

        def test_thread_local_data(self):
            """
            `线程局部数据 <https://docs.python.org/zh-cn/3/library/threading.html#thread-local-data>`_：Thread-local data
            """
            local_data = threading.local()
            threads = []

            def worker(name):
                local_data.name = name
                print(f"线程: {threading.current_thread().name}, 名字: {local_data.name}")

            threads.append(threading.Thread(target=worker, args=("Alice",), name="T1"))
            threads.append(threading.Thread(target=worker, args=("Bob",), name="T2"))
            for t in threads: t.start()
            for t in threads: t.join()

        class BankAccount:
            def __init__(self):
                self._balance = 0
                self._lock = threading.RLock()
                self._spin_lock = threading.Lock()
                self._semaphore = threading.Semaphore(2)
                self._event = threading.Event()
                self._event.set()

            def lock_deposit(self, amount):
                self._lock.acquire()
                try:
                    self._deposit(amount)
                finally:
                    self._lock.release()

            def lock_deposit_v2(self, amount):
                with self._lock:
                    self._deposit(amount)

            # threading.Lock + 自旋等待，模拟 .NET SpinLock
            def spin_lock_deposit(self, amount):
                while not self._spin_lock.acquire(blocking=False):
                    # 小延迟避免 CPU 占用过高
                    time.sleep(0.0001)
                try:
                    self._deposit(amount)
                finally:
                    self._spin_lock.release()

            def semaphore_deposit(self, amount):
                with self._semaphore:
                    self._deposit(amount)

            def event_deposit(self, amount):
                self._event.wait()
                try:
                    self._deposit(amount)
                finally:
                    self._event.clear()
                    self._event.set()

            def _deposit(self, amount: int):
                logger.info(f"正在存款 {amount} 到账户，当前余额: {self._balance}")
                time.sleep(0.01)
                self._balance += amount
                logger.info(f"存款完成，新的余额: {self._balance}")

        def test_synchronization_objects(self):
            """ 同步对象 """
            account = self.BankAccount()
            sync_methods = [
                account.lock_deposit,
                account.lock_deposit_v2,
                account.spin_lock_deposit,
                account.semaphore_deposit,
                account.event_deposit,
            ]
            threads = [threading.Thread(target=method, args=(100,)) for method in sync_methods]
            for thread in threads: thread.start()
            for thread in threads: thread.join()
            logger.info("所有存款操作已完成")

    class TestMultiprocessing:
        """
        `基于进程的并行 <https://docs.python.org/zh-cn/3/library/multiprocessing.html>`_：
            通过使用子进程而非线程有效地绕过`全局解释器锁 <#gil>`_；适用于 CPU 密集型任务

        Process 和 Thread API 相同

        注：Python 用多进程实现并行，Java/.NET 用多线程即可实现并行
        """

        @staticmethod
        def producer(queue):
            for i in range(5):
                queue.put(f"Task {i}")
                print(f"Produced Task {i}")

        @staticmethod
        def consumer(queue):
            while True:
                task = queue.get()
                if task == 'STOP':
                    break
                print(f"Consumed {task}")

        @staticmethod
        def child(conn):
            conn.send("Hello from child process")
            print(conn.recv())
            conn.close()

        @staticmethod
        def incr(val):
            with val.get_lock():
                val.value += 1

        @staticmethod
        def update_list(shared_list, index, value):
            shared_list[index] = value

        def test_inter_process_communication(self):
            """ 进程间通信 """
            from multiprocessing import Process, Queue, Pipe, Value, Manager

            # region 1. Queue：生产者-消费者
            queue = Queue()
            p1 = Process(target=self.producer, args=(queue,))
            p2 = Process(target=self.consumer, args=(queue,))
            p1.start()
            p2.start()
            p1.join()
            queue.put('STOP')
            p2.join()
            # endregion

            # region 2. Pipe：点对点（监听器-客户端）
            parent_conn, child_conn = Pipe()
            p = Process(target=self.child, args=(child_conn,))
            p.start()
            print(parent_conn.recv())
            parent_conn.send("Hello back")
            p.join()
            # endregion

            # region 3. Value、Array：共享简单变量或数组
            counter = Value('i', 0)
            processes = [Process(target=self.incr, args=(counter,)) for _ in range(10)]
            for p in processes: p.start()
            for p in processes: p.join()
            print(counter.value)
            # endregion

            # region 4. Manager()：共享复杂对象
            with Manager() as manager:
                shared_list = manager.list([0] * 10)
                processes = [Process(target=self.update_list, args=(shared_list, i, i * 2)) for i in range(10)]
                for p in processes: p.start()
                for p in processes: p.join()
                print(list(shared_list))
            # endregion

        def test_pool(self):
            """ 工作进程池 """
            with multiprocessing.Pool(processes=4) as pool:
                assert pool.map(abs, range(10)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

                results = [pool.apply_async(os.getpid) for _ in range(1000)]
                # 集合推导式去重
                print({result.get(timeout=1) for result in results})

    def test_concurrent_futures(self):
        """
        `启动并行任务 <https://docs.python.org/zh-cn/3/library/concurrent.futures.html>`_：提供异步执行可调用对象高层接口

        1. ThreadPoolExecutor：Executor 子类，使用线程池来异步执行调用
        2. ProcessPoolExecutor：Executor 子类，使用进程池来异步执行调用
        3. Future：将可调用对象封装为异步执行
        """


# endregion
# region 网络和进程间通信：https://docs.python.org/zh-cn/3/library/ipc.html
class TestNetworkingAndInterprocessCommunication:
    class TestAsyncio:
        """
        `异步 I/O <https://docs.python.org/zh-cn/3/library/asyncio.html>`_：

        1. 用来编写并发代码的库，使用 async/await 语法
        2. 被用作多个提供高性能 Python 异步框架的基础，包括网络和网站访问，数据库连接库，分布式任务队列等
        3. 构建 IO 密集型和高层级结构化网络代码的最佳选择
        """

        class TestCoroutinesAndTasks:
            """
            `协程和任务 <https://docs.python.org/zh-cn/3/library/asyncio-task.html>`_：
                使用 async/await 语法声明的协程是编写 asyncio 应用程序的首选方式

            实现方式：

            1. 内置：asyncio + async def/await，基于事件循环机制
            2. 第三方：

                1. `greenlet <https://pypi.org/project/greenlet/>`_：进程内并发编程的轻量级协程（需显式切换）
                2. `gevent <https://pypi.org/project/gevent/>`_：基于协程的网络库，它使用 greenlet 在 libev 或 libuv 事件循环之上提供高级同步API（自动调度）
            """

            @staticmethod
            async def say_after(what, delay=0.1):
                await asyncio.sleep(delay)
                print(what)

            def test_coroutines(self):
                async def main():
                    print(f"started at {time.strftime('%X')}")
                    await self.say_after('hello')
                    await self.say_after('world')
                    print(f"finished at {time.strftime('%X')}")

                asyncio.run(main())

            @pytest.mark.asyncio
            async def test_coroutines2(self):
                print(f"started at {time.strftime('%X')}")
                await asyncio.create_task(self.say_after('hello'))
                await asyncio.create_task(self.say_after('world'))
                print(f"finished at {time.strftime('%X')}")

            @pytest.mark.asyncio
            async def test_coroutines3(self):
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(self.say_after('hello'))
                    tg.create_task(self.say_after('world'))
                    print(f"started at {time.strftime('%X')}")
                print(f"finished at {time.strftime('%X')}")

            def test_coroutines_by_gevent(self):
                """
                gevent.monkey.patch_all()：将标准库中的阻塞操作（如 socket、threading、time）替换为协作式调度版本，使同步代码可在 gevent 协程中并发运行

                1. 需尽早调用：在程序导入任何其他模块之前调用
                2. 避免 multiprocessing 阻塞操作：如 ProcessPoolExecutor.result()、Queue.get()，因其会阻塞系统调用，冻结事件循环
                """
                import gevent
                def say_after(what, delay=0.1):
                    gevent.sleep(delay)
                    print(what)

                print(f"started at {time.strftime('%X')}")
                task1 = gevent.spawn(say_after, 'hello')
                task2 = gevent.spawn(say_after, 'world')
                gevent.joinall([task1, task2])
                print(f"finished at {time.strftime('%X')}")


# endregion
# region 互联网数据处理：https://docs.python.org/zh-cn/3/library/netdata.html
class TestInternetDataHandling:
    def test_json(self):
        data = {"name": "张三", "age": 30, "skills": ["Python", "Data Science"]}
        # ensure_ascii  对非 ASCII 字符进行转义
        # sort_keys     按键排序
        json_str = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
        print(json_str)
        assert json.loads(json_str) == data
        with open("test.json", "w+", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.seek(0)
            assert json.load(f) == data

    def test_base64(self):
        """
        Base16, Base32, Base64, Base85 数据编码
        """
        import base64
        data = '123'.encode()
        # 加密
        base64_str = base64.b64encode(data).decode()
        print(base64_str)
        # 解密
        assert base64.b64decode(base64_str) == data


# endregion
# region 互联网协议和支持：https://docs.python.org/zh-cn/3/library/internet.html
class TestInternetProtocolsAndSupport:
    def test_urllib_parse(self):
        """
        `将 URL 解析为组件 <https://docs.python.org/zh-cn/3/library/urllib.parse.html>`_：
            将统一资源定位符（URL）字符串拆分为不同部分（协议、网络位置、路径等），或将各个部分组合回 URL 字符串，并将“相对 URL”转换为基于给定的“基准 URL”的绝对 URL
        """
        from urllib.parse import quote, unquote, urlparse
        # region urlparse
        o = urlparse('http://docs.python.org:80/3/library/urllib.parse.html?highlight=params#url-parsing')
        assert o.scheme == 'http'
        assert o.netloc == 'docs.python.org:80'
        assert o.hostname == 'docs.python.org'
        assert o.port == 80
        assert o.path == '/3/library/urllib.parse.html'
        assert o.params == ''
        assert o.query == 'highlight=params'
        assert o.fragment == 'url-parsing'
        # endregion
        s = '爬虫'
        assert unquote(quote(s)) == s


# endregion
# region 通用操作系统服务：https://docs.python.org/zh-cn/3/library/allos.html
class TestGenericOperatingSystemServices:
    class TestOS:
        """
        `多种操作系统接口 <https://docs.python.org/zh-cn/3/library/os.html>`_

        适用性说明：

        1. 只要某个功能在多个操作系统上都可用，Python 就会提供一个统一的接口，让你用相同的方式调用它
        2. 所有接受路径或文件名的函数都同时支持字节串和字符串对象，并在返回路径或文件名时使用相应类型的对象作为结果
        """

        def test_os(self):
            # 导入的操作系统相关模块的名称：'posix', 'nt', 'java'
            assert os.name == 'nt'
            # 环境变量
            assert os.environ['OS'] == os.getenv('OS') == r'Windows_NT'
            # 当前进程 ID，父进程 ID
            print(os.getpid(), os.getppid())
            # 逻辑 CPU 数量
            assert os.cpu_count() == 12
            # 分隔路径的字符：POSIX 是 '/'，WINDOWS 是 '\\'
            assert os.sep == '\\'
            assert os.altsep == '/'
            # 分隔搜索路径的字符：POSIX 是 ':'，WINDOWS 是 ';'
            assert os.pathsep == ';'
            # 分隔基本文件名和扩展名的字符
            assert os.extsep == '.'
            # 分隔（终止）行的字符：POSIX 是 '\n'，WINDOWS 是 '\r\n'
            assert os.linesep == '\r\n'

        def test_files_and_directories(self):
            print(f"当前工作目录：{os.getcwd()}")
            print(f"目录下文件的名称：{os.listdir()}")
            # 目录树生成器
            for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
                print(dirpath)
                for dirname in dirnames: print(os.path.join(dirpath, dirname))
                for filename in filenames: print(os.path.join(dirpath, filename))
                print()

            new_dir = "test_dir"
            if not os.path.exists(new_dir):
                # 创建目录
                os.mkdir(new_dir)
            # 改变工作目录
            # os.chdir(new_dir)
            # 删除目录
            os.rmdir(new_dir)
            # 递归创建目录，即使目录已存在
            os.makedirs(new_dir, exist_ok=True)
            file_path = os.path.join(new_dir, "empty.txt")
            # 创建一个文件
            with open(file_path, "w"):
                pass
            new_file_path = os.path.join(new_dir, "new_file.txt")
            # 重命名文件
            os.rename(file_path, new_file_path)
            # 删除文件，语义与 os.unlink() 相同
            os.remove(new_file_path)
            # 递归删除目录
            os.removedirs(new_dir)

        def test_process_management(self):
            # 在子 shell 中执行操作系统命令
            os.system('cmd')
            os.system('regedit')
            os.system('ping www.baidu.com')

            # 使用已关联的应用程序打开文件
            os.startfile('test.txt')

    class TestIO:
        """
        三种 I/O 类型：

        1. 文本 I/O：期望并生成 str 对象；按照指定的编码格式自动处理编码解码、按照操作系统自动转换换行符

            1. TextIOBase：TextIOWrapper、StringIO
            2. 人类可读文本
            3. `open("test.txt", "r", encoding="utf-8")`

        2. 二进制 I/O：缓冲 I/O，接收 字节型对象 并生成 bytes 对象；不执行编码、解码、换行符转换

            1. BufferedIOBase：BytesIO、BufferedReader、BufferedWriter、BufferedRandom
            2. 非文本数据（图像/音视频/压缩文件）；网络通信；性能敏感场景（大文件、数据流）；需减少系统调用场景（频繁的小数据读写）
            3. `open("test.txt", "rb")`

        3. 原始 I/O：非缓冲 I/O，通常用作二进制和文本流的低级构建块

            1. RawOIOBase：FileIO
            2. 底层设备交互；需精确控制 I/O 行为（实时系统、设备驱动程序）；零拷贝数据处理（内存映射、数据库页直接访问）；特殊存储需求（自定义文件系统、日志结构存储）；I/O 行为分析（基准测试、性能分析）
            3. `open("test.txt", "rb", buffering=0)`
        """

        def test_io(self):
            with open("test.txt", "r", encoding="utf-8") as f:
                assert f.name == "test.txt"
                assert f.mode == "r"
                assert f.readline() == "静夜思\n"

        def test_bytesio(self):
            """ BytesIO：使用内存字节缓冲区的二进制流 """
            from io import BytesIO
            b = BytesIO(b"abcdef")
            view = b.getbuffer()
            view[2:4] = b"34"
            assert view == b"ab34ef"

    def test_time(self):
        """
        `时间的访问和转换 <https://docs.python.org/zh-cn/3/library/time.html>`_

        时间格式：

        1. 时间戳 float(seconds)
        2. 元组   struct_time
        3. 字符串 str
        """
        import calendar

        # 当前时间戳：返回以浮点数表示的从 epoch 开始的秒数形式的时间
        print(time.time())

        # epoch 起始的时间点
        t = time.gmtime(0)

        # region float → struct_time
        assert time.gmtime(0)[:9] == (1970, 1, 1, 0, 0, 0, 3, 1, 0)
        local_t = time.localtime(0)
        assert local_t[:9] == (1970, 1, 1, 8, 0, 0, 3, 1, 0)
        # endregion

        # region struct_time → float
        # localtime() 的反函数
        assert time.mktime(local_t) == 0
        assert calendar.timegm(t) == 0
        # endregion

        # region float → str
        assert time.ctime(0) == 'Thu Jan  1 08:00:00 1970'
        # endregion

        # region struct_time → str
        assert time.asctime(t) == 'Thu Jan  1 00:00:00 1970'
        time_format = '%Y-%m-%d, %H:%M:%S %Z'
        formatted = time.strftime(time_format, t)
        assert formatted == '1970-01-01, 00:00:00 中国标准时间'
        # endregion

        # region str → struct_time
        assert time.strptime(formatted, time_format) == t
        # endregion

        # region struct_time 属性
        assert t.tm_year == 1970
        assert t.tm_mon == 1
        assert t.tm_mday == 1
        assert t.tm_hour == 0
        assert t.tm_min == 0
        assert t.tm_sec == 0
        assert t.tm_wday == 3
        assert t.tm_yday == 1
        assert t.tm_isdst == 0
        assert t.tm_zone == 'UTC'
        assert t.tm_gmtoff == 0
        # endregion


# endregion
# region Python 运行时服务：https://docs.python.org/zh-cn/3/library/python.html
class TestPythonRuntimeServices:
    def test_sys(self):
        """
        `系统相关的形参和函数 <https://docs.python.org/zh-cn/3/library/sys.html>`_
        """
        import sys
        # 命令行参数
        assert sys.argv[1] == 'test_syntax.py::TestPythonRuntimeServices::test_sys'
        # Python 模块搜索路径
        assert sys.path[0] == r'D:\Liang\git\python\tests'
        # 平台标识
        assert sys.platform == 'win32'
        # Python 版本
        assert sys.version_info > (3, 8)
        # 标准输入输出流
        sys.stdout.write("Hello\n")
        sys.stderr.write("Error message\n")
        # 已加载模块
        assert sys.modules['sys'] is sys
        # 获取对象内存大小
        assert sys.getsizeof(1) == 28
        # Python 解释器路径
        assert sys.executable == r'D:\Python\Python313\python.exe'
        # 获取系统用于文件系统编码的编码方式
        assert sys.getfilesystemencoding() == "utf-8"
        # 主 Python 解析器是否正在关闭
        assert sys.is_finalizing() is False
        # 引发一个 SystemExit 异常，表示打算退出解释器
        try:
            sys.exit()
        except SystemExit:
            pass

    def test_dataclasses(self):
        """
        `dataclasses <https://docs.python.org/zh-cn/3/library/dataclasses.html>`_：
            提供了一个装饰器和函数，用于自动将生成的特殊方法添加到用户定义的类中
        """
        from dataclasses import asdict, astuple, dataclass, field, InitVar, is_dataclass, KW_ONLY

        @dataclass
        class Base:
            id: Any = field(kw_only=True, default=None)
            name: Any

        @dataclass
        # 继承：按反向 MRO 顺序（从 object 开始）查看它的所有基类，并将找到的每个字段添加到一个有序映射中。
        # 此例最终的字段列表一次是：id, name, interest, birth_year, age
        # 所有生成的方法都将使用这个有序映射
        # 注：由于 __init()__ 中仅限关键字形参的重新排序，所以在 __init()__ 中的顺序是 name, id, interest, birth_year, age
        class P(Base):
            name: str
            # KW_ONLY 类型的伪字段之后的任何字段都标记为仅限关键字字段
            _: KW_ONLY
            interest: list[int] = field(default_factory=list)
            # InitVar：仅限初始化变量，不会成为正式字段（不会出现在实例属性中），用于 __post_init__()
            birth_year: InitVar[int | None] = None
            age: int = 0

            # 将被生成的 __init__() 调用
            def __post_init__(self, birth_year):
                current_year = datetime.datetime.now().year
                self.age = current_year - birth_year

        # 使用 inspect.signature() 查看生成的 __init__()
        assert (str(inspect.signature(P.__init__)) ==
                '(self, name: str, *, id: Any = None, interest: list[int] = <factory>, birth_year: dataclasses.InitVar[int | None] = None, age: int = 0) -> None')
        p1 = P('A', id=0, birth_year=1999)
        p2 = P('B', id=1, birth_year=2001)
        assert id(p1.interest) != id(p2.interest)
        # 将数据类对象转换为字典（使用工厂函数 dict_factory）
        assert asdict(p1) == {'id': 0, 'name': 'A', 'interest': [], 'age': 26}
        # 将数据类对象转换为元组（使用工厂函数 tuple_factory）
        assert astuple(p1) == (0, 'A', [], 26)
        # 判断是否是 dataclass 或其实例
        assert is_dataclass(p1)
        # 判断是否为 dataclass 的实例
        assert is_dataclass(p1) and not isinstance(p1, type)


# endregion
# region 数据模型：https://docs.python.org/zh-cn/3/reference/datamodel.html
class TestDataModel:
    class TestTheStandardTypeHierarchy:
        """
        `标准类型层级结构 <https://docs.python.org/zh-cn/3/reference/datamodel.html#the-standard-type-hierarchy>`_

        8. 可调用类型：可以被应用于函数调用操作，:class:`TestCallableTypes`
        11. 类实例：:class:`TestClassInstances`
        """

        class TestCallableTypes:
            def test_attributes(self):
                # 函数的文档字符串
                assert self.__doc__ is None
                # 函数所属模块的名称
                assert self.__module__ == 'test_syntax'

        class TestClassInstances:
            def test_special_attributes(self):
                # 类实例所属的类
                assert self.__class__.__name__ == 'TestClassInstances'
                # 一个用于存储对象的（可写）属性的字典或其他映射对象
                assert self.__dict__ == {}

    class TestSpecialMethodNames:
        """
        `特殊方法名称 <https://docs.python.org/zh-cn/3/reference/datamodel.html#special-method-names>`_：
            一个类通过定义具有特殊名称的方法来实现由特殊语法来唤起的特定操作
        """

        class TestBasicCustomization:
            """
            基本定制

            - object.__del__(self)：在实例被销毁时调用
            - object.__repr(self)：:func:`TestBuiltinFunctions.test_repr_str`
            - object.__str__(self)：:func:`TestBuiltinFunctions.test_repr_str`
            """

            def test_new(self):
                """
                object.__new__(cls[, ...])：

                1. 典型的实现：使用 super().__new__(cls[, ...]) 创建一个新的类实例，在返回它之前根据需求对其进行修改
                2. 分配内存空间
                3. 返回对象实例：①返回一个 cls 的实例，将唤起 __init__()；②未返回 cls 的实例，跳过 __init__()
                4. 使用场景：单例、对象池、不可变对象、自定义元类
                """

                class Singleton:
                    obj = None

                    def __new__(cls, *args, **kwargs):
                        if cls.obj is None:
                            cls.obj = super().__new__(cls)
                        return cls.obj

                assert Singleton() == Singleton()

        class TestCustomizingAttributeAccess:
            """ 自定义属性访问 """

            def test_slots(self):
                """
                object.__slots__

                1. 允许我们显示地声明数据成员，并禁止创建 __dict__ 和 __weakref__（除非在 __slots__ 中显示地声明或是在父类中可用）
                2. 相比 __dict__ 显著节省空间，显著提升属性查找速度
                3. 可赋值为：字符串、可迭代对象、由实例使用的变量名组成的字符串序列
                """

        def test_emulating_callable_objects(self):
            """
            object.__call__(self[, args...])：模拟可调用对象，此方法在实例作为一个函数被调用时被调用
            """

            class A:
                def __call__(self):
                    return A.__name__

            assert A()() == A.__name__


# endregion
# region 表达式：https://docs.python.org/zh-cn/3/reference/expressions.html
# 运算符：https://docs.python.org/zh-cn/3/reference/lexical_analysis.html#operators
class TestExpressions:
    def test_expressions(self):
        # 除法结果是 float
        assert type(6 / 2) == float
        # 整除
        assert 7.0 // 2 == 3
        assert type(7 // 2) == int
        assert type(7.0 // 2) == float
        # 幂运算
        assert 2 ** 3 == 8
        # 条件表达式/三目运算
        assert 1 if True else 0 == 1

    def test_generator(self):
        # 生成器表达式
        even_squares = (i ** 2 for i in range(10) if i % 2 == 0)

        # 生成器函数
        def generate_even_squares(n):
            for i in range(n):
                if i % 2 == 0:
                    received = yield i ** 2
                    print(i, received)

        gen = generate_even_squares(10)

        assert next(gen) == 0
        assert next(gen) == 4
        assert gen.send(100) == 16

        assert list(even_squares) == list(generate_even_squares(10))


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
# region 控制流工具：https://docs.python.org/zh-cn/3/tutorial/controlflow.html
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
# region 数据结构：https://docs.python.org/zh-cn/3/tutorial/datastructures.html
class TestDataStructures:
    def test_sets(self):
        """
        `集合 <https://docs.python.org/zh-cn/3/tutorial/datastructures.html#sets>`_
        """
        a = set('watermelon')
        b = set('pineapple')
        # 差集
        assert a - b == {'m', 'o', 'w', 'r', 't'}
        # 并集
        assert a | b == {'l', 'o', 'e', 't', 'n', 'p', 'i', 'a', 'm', 'r', 'w'}
        # 交集
        assert a & b == {'e', 'l', 'a', 'n'}
        # 对称差集
        assert a ^ b == {'i', 'o', 'w', 't', 'm', 'p', 'r'}


# endregion
# region 模块：https://docs.python.org/zh-cn/3/tutorial/modules.html
class TestModules:
    def test__modules(self):
        """
        模块是天然的单例

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
    """
    类

    命名空间生命周期

    1. 内置名称的命名空间：在 Python 解释器启动时创建的，永远不会被删除
    2. 模块的命名空间：在读取模块定义时创建
    3. 函数的局部命名空间：在函数被调用时创建；在函数返回或抛出未在函数内被处理的异常时删除

    作用域：

    1. L：Local，最内层作用域，包含局部名称
    2. E：Enclosing，外层闭包函数的作用域，包含“非局部、非全局”的名称
    3. G：Global，当前模块的全局名称
    4. B：Built-in，内置名称的命名空间
    """

    def test_multiple_inheritance(self):
        """
        多重继承

        1. 搜索父类属性的操作可以认为是 深度优先、从左到右
        2. `Python 2.3 方法解析顺序 <https://docs.python.org/zh-cn/3/howto/mro.html>`_
        """

        class A:
            def m(self):
                return 'A'

        class B(A):
            def m(self):
                return 'B'

        class C(A):
            def m(self):
                return 'C'

        class D(B, C): pass

        # Method Resolution Order，方法解析顺序
        assert D.__mro__ == (D, B, C, A, object)
        assert D().m() == 'B'

    def test_private_variables(self):
        """
        非公有部分：约定，带有一个下划线开头的标识符

        私有名称：private name, 以两个或更多下划线开头，最多一个下划线结尾的标识符

        私有名称改写：__spam → _classname__name
        """

        class Person:
            def __init__(self, name, id_number):
                self.name = name
                self._age = None
                self.__id_number = id_number

        p = Person("Mary", "123")
        assert p.name == "Mary"
        # 可访问单下划线开头属性，不推荐直接访问
        assert p._age is None
        # 私有名称改写，不推荐直接访问
        assert p._Person__id_number == "123"  # type: ignore[attr-defined]


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

        from types import FunctionType
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

        def test_function_decorator(self):
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
