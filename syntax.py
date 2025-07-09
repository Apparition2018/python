"""
语法基础

- Python      强类型动态语言
- Java        强类型静态语言
- JavaScript  弱类型动态语言
"""

# region 内置函数：https://docs.python.org/zh-cn/3.13/library/functions.html
# print()
print("广州", "深圳", "中山", sep=" ", end="\n")
print("""A
B""")
# range(), sum()
result = 0
r = range(1, 101, 1)
for i in r:
    result += i
assert result == sum(r)
# endregion

# region 内置类型：https://docs.python.org/zh-cn/3.13/library/stdtypes.html
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

# region 序列类型：https://docs.python.org/zh-cn/3.13/library/stdtypes.html#sequence-types-list-tuple-range
# 元组和序列：https://docs.python.org/zh-cn/3.13/tutorial/datastructures.html#tuples-and-sequences
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

# region Set类型：https://docs.python.org/zh-cn/3.13/library/stdtypes.html#set-types-set-frozenset
"""
不同可哈希对象的无序集合

两种内置 Set：
    1. set：可变的，所以没有哈希值；不能被用作字典的键或其他 set 的元素
    2. frozenset：不可变且可哈希；可以被用作字典的键或其他 set 的元素
"""
# 空 Set
s = set()
s.add('a')
s.add('b')
s.add('c')
s.add('d')
s.add('e')
s.remove('e')
assert s == {'d', 'c', 'b', 'a'}
# 存在则移除
s.discard('f')
assert s == {'d', 'c', 'b', 'a'}
# 移除并返回左一元素
s.pop()
# 由于 int 哈希值等于其本身，所以此 set ‘实现了有序’，左一元素永远是1
assert {1, 2, 3}.pop() == 1
# endregion

# region 映射类型：https://docs.python.org/zh-cn/3.13/library/stdtypes.html#mapping-types-dict
d = {'name': 'ljh', 'age' : 18}
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

# region 运算
# 运算符：https://docs.python.org/zh-cn/3.13/reference/lexical_analysis.html#operators
# 表达式：https://docs.python.org/zh-cn/3.13/reference/expressions.html
# 除法结果是 float
assert type(6 / 2) == float
# 整除
assert 7.0 // 2 == 3
assert type(7 // 2) == int
assert type(7.0 // 2) == float
# 幂运算
assert 2 ** 3 == 8
# endregion 运算

# region 格式化字符串
# 更复杂的输出格式：https://docs.python.org/zh-cn/3.13/tutorial/inputoutput.html#fancier-output-formatting
year = 2025
month = 7
day = 2
assert "Today is %d-%02d-%02d" % (year, month, day) == "Today is 2025-07-02"
assert f"Today is {year}-{month:02d}-{day:02d}" == "Today is 2025-07-02"
# endregion
