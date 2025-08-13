# 并发执行：https://docs.python.org/zh-cn/3/library/concurrency.html
import threading
import time

from loguru import logger


def crawl(link, method):
    logger.info(f"crawl started for {link} by {method}")
    time.sleep(0.01)
    logger.info(f"crawl ended for {link} by {method}")


links = [
    "https://python.org",
    "https://docs.python.org",
    "https://peps.python.org",
]


def test_concurrency():
    from threading import Thread
    from multiprocessing import Process
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

    # region：Thread
    threads = []
    for link in links:
        t = Thread(target=crawl, args=(link,), kwargs={"method": "Thread"})
        threads.append(t)
    for t in threads: t.start()
    for t in threads: t.join()
    # endregion

    # region：Process
    processes = []
    for link in links:
        p = Process(target=crawl, args=(link,), kwargs={"method": "Process"})
        processes.append(p)
    for p in processes: p.start()
    for p in processes: p.join()
    # endregion

    # region：ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:
        [executor.submit(crawl, link, "ThreadPoolExecutor") for link in links]
    # endregion

    # region：ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=3) as executor:
        [executor.submit(crawl, link, "ProcessPoolExecutor") for link in links]
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

    def test_timer(self):
        """
        `Timer <https://docs.python.org/zh-cn/3/library/threading.html#timer-objects>`_：定时器，Thread 的子类
        """
        interval = 0.1
        for link in links:
            threading.Timer(interval, crawl, args=(link,), kwargs={"method": "timer"}).start()
        time.sleep(interval * len(links))


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
        import os
        from multiprocessing import Pool
        with Pool(processes=4) as pool:
            assert pool.map(abs, range(10)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

            results = [pool.apply_async(os.getpid) for _ in range(1000)]
            # 集合推导式去重
            print({result.get(timeout=1) for result in results})


def test_concurrent_futures():
    """
    `启动并行任务 <https://docs.python.org/zh-cn/3/library/concurrent.futures.html>`_：提供异步执行可调用对象高层接口

    1. ThreadPoolExecutor：Executor 子类，使用线程池来异步执行调用
    2. ProcessPoolExecutor：Executor 子类，使用进程池来异步执行调用
    3. Future：将可调用对象封装为异步执行
    """
