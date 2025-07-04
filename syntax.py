"""
语法基础

- Python      强类型动态语言
- Java        强类型静态语言
- JavaScript  弱类型动态语言
"""

# region print()
print("广州", "深圳", "中山", sep=" ", end="\n")
print("""A
B""")
# endregion

# region 格式化字符串
year = 2025
month = 7
day = 2
assert "Today is %d-%02d-%02d" % (year, month, day) == "Today is 2025-07-02"
assert f"Today is {year}-{month:02d}-{day:02d}" == "Today is 2025-07-02"
# endregion

# region 其它
# bool 是 int 子类，False 和 True 的行为分别与整数 0 和 1 类似，但是不建议这样使用
assert True + False == 1

# 除法结果总是 float
assert type(7 / 2) == float
# 向下取整除法
assert 7.0 // 2 == 3
assert type(7 // 2) == int
assert type(7.0 // 2) == float
# 幂运算
assert 2 ** 3 == 8

# range(), sum()
result = 0
r = range(1, 101, 1)
for i in r:
    result += i
assert result == sum(r)
# endregion

# region 序列
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
# 切片操作
assert "watermelon"[0:5] == "water"
assert "watermelon"[-5:] == "melon"
assert "watermelon"[-1:-3:-1] == "no"
assert len("hello") == 5
assert "a" * 3 == "aaa"
assert "water" in "watermelon"
assert "fire" not in "watermelon"
# endregion

# region 字符串方法
# find() 未找到到返回 -1，index() 未找到引发 ValueError
assert "watermelon".find("melon") == "watermelon".index("melon")
assert "banana".count("a") == 3
assert "blood".replace("o", "e") == "bleed"
# encode(), decode()
h_encode = "hello".encode("utf8")
assert h_encode == b'hello'
assert h_encode.decode("utf8") == "hello"
# endregion
