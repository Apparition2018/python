import time
from typing import Callable, Any


class Timer:
    @staticmethod
    def measure(func: Callable, *args, **kwargs) -> tuple[Any, float]:
        """
        测量函数执行时间

        Parameters
        ----------
        func: 要测量的函数
        *args, **kwargs: 函数参数

        Returns
        -------
        元组 (执行时间(秒)，函数结果)
        """
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return end - start, result
