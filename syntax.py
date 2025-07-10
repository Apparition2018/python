"""
语法基础

- Python      强类型动态语言
- Java        强类型静态语言
- JavaScript  弱类型动态语言
"""
import copy

# region 内置函数：https://docs.python.org/zh-cn/3/library/functions.html
# print()
print("广州", "深圳", "中山", sep=" ", end="\n")
print("""广州
深圳
中山""")
# id()：返回对象内存地址
id(1)
# range(), sum()
result = 0
r = range(1, 101, 1)
for i in r:
    result += i
assert result == sum(r)
# 类型转换：int(), float(), char(), str(), tuple(), list(), eval()
assert int(1.8) == 1
assert list('hello') == ['h', 'e', 'l', 'l', 'o']
assert list({'name': 'ljh', 'age': 18}) == ['name', 'age']
assert eval('1+1') == 2
assert type(eval('[1, 2, 3]')) == list
# endregion

# region 内置类型：https://docs.python.org/zh-cn/3/library/stdtypes.html
"""
不可变类型：修改操作实际创建新对象，内存地址改变，可用作字典键
    1. 数值：int, flot, complex, bool
    2. 文本序列：str
    3. 序列：tuple，range
    4. 二进制序列：bytes
    5. 集合：frozenset

可变类型：支持原地修改，不可用作字典键
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
# 移除
del seq[len(seq) - 1]
assert seq == ['a', 'b', 'c', 'd', 'e', 'f']
seq.pop()
seq.pop(len(seq) - 1)
assert seq == ['a', 'b', 'c', 'd']
seq.remove('d')
assert seq == ['a', 'b', 'c']
# 列表推导式
assert [x * 2 for x in range(1, 10) if x <= 3] == [2, 4, 6]
# 元组只有一个元素时，type()返回元素的类型，而不是元组类型
assert type((1)) == int
assert type((1,)) == tuple
# endregion

# region 内置类型-集合类型：https://docs.python.org/zh-cn/3/library/stdtypes.html#set-types-set-frozenset
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
d = {'name': 'ljh', 'age': 18}
assert type(d) == dict
assert len(d) == 2
# keys()、values()、items() 返回的对象是试图对象
assert type(d.keys()).__name__ == 'dict_keys'
assert type(d.values()).__name__ == 'dict_values'
assert type(d.items()).__name__ == 'dict_items'
del d['age']
d['age'] = 123
d.pop('age')
d['age'] = 123
assert d.popitem() == ('age', 123)
d.clear()
assert d == {}
# 字典推导式
assert {x: x ** 2 for x in range(1, 10) if x <= 3} == {1: 1, 2: 4, 3: 9}
# endregion

# region 数据类型-copy：https://docs.python.org/zh-cn/3/library/copy.html
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
# 除法结果是 float
assert type(6 / 2) == float
# 整除
assert 7.0 // 2 == 3
assert type(7 // 2) == int
assert type(7.0 // 2) == float
# 幂运算
assert 2 ** 3 == 8
# endregion 运算

# region 控制流程工具-定义函数
"""
1. `简介 <https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions>`_
2. `更多 <https://docs.python.org/zh-cn/3/tutorial/controlflow.html#more-on-defining-functions>`_
"""


def return1():
    """没有返回值，返回 None"""
    pass


def return2():
    """一个返回值，返回该值"""
    return 1


def return3():
    """多个返回值，返回元组"""
    return 1, 2, 3


assert return1() is None
assert len((return2(),)) == 1
assert len(return3()) > 1


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


def func2(kind, *pos, **kwd):
    """
    `任意参数列表 <https://docs.python.org/zh-cn/3/tutorial/controlflow.html#arbitrary-argument-lists>`_

    :param kind:
    :param pos: 接受一个元组，包含形参列表之外的位置参数；该形参后只能是仅限关键字参数
    :param kwd: 接受一个字典，包含形参列表之外的关键字参数
    """
    pass


func2(1, 2, 3, 4, kwd1=5, kwd2=6)
r = range(2, 5)
d = {"kwd1": 5, "kwd2": 6}
"""
`解包实参列表 <https://docs.python.org/zh-cn/3/tutorial/controlflow.html#unpacking-argument-lists>`_
"""
func2(1, *r, **d)
# endregion

# region 输入与输出-格式化字符串
# 更复杂的输出格式：https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#fancier-output-formatting
year = 2025
month = 7
day = 2
assert "Today is %d-%02d-%02d" % (year, month, day) == "Today is 2025-07-02"
assert f"Today is {year}-{month:02d}-{day:02d}" == "Today is 2025-07-02"
# endregion
