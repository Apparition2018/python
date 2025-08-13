# pytest 钩子函数，在 pytest 启动时被调用
from gevent import monkey


def pytest_configure():
    # 态修改 Python 标准库中的阻塞函数，让它们变成非阻塞的，从而实现高并发
    monkey.patch_all()
