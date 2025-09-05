""" packages：https://pypi.org/ """
import json
import logging
import os
import random
import re
import time

import requests
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt


class TestRequests:
    """
    `requests <https://pypi.org/project/requests/>`_：HTTP 库
    """

    def test_basic(self):
        r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
        r.raise_for_status()
        assert r.status_code == 200
        assert r.headers['content-type'] == 'application/json'
        assert r.encoding == 'utf-8'
        # 响应内容（字节）
        assert r.content == b'{\n  "authenticated": true, \n  "user": "user"\n}\n'
        assert r.text == r.content.decode(r.encoding) == '{\n  "authenticated": true, \n  "user": "user"\n}\n'
        assert r.json() == json.loads(r.text) == {'authenticated': True, 'user': 'user'}

    def test_advance(self):
        from requests.adapters import HTTPAdapter
        from urllib3 import Retry
        # 会话
        with requests.Session() as session:
            # 连接池
            adapter = HTTPAdapter(
                pool_connections=15,
                pool_maxsize=50,
                # 重试
                max_retries=Retry(total=3, backoff_factor=0.5)
            )
            session.mount("https://", adapter)
            r = session.get(
                'https://2025.ip138.com/',
                headers={'User-Agent': UserAgent().random},
                # 代理：https://free.kuaidaili.com/free/dps/
                # proxies={"https": "180.121.147.240:20756"},
                timeout=2,
                allow_redirects=True
            )
            print(re.search(r'<title[^>]*>.*?(\d+(?:\.\d+)*)', r.text).group(1).strip())


def test_user_agent():
    """
    `fake-useragent <https://pypi.org/project/fake-useragent/>`_：useragent faker
    """
    from fake_useragent import UserAgent
    url = 'https://www.baidu.com'
    r = requests.get(url)
    # 1. 自定义随机 User-Agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
    ]
    r2 = requests.get(url, headers={'User-Agent': random.choice(user_agents)})
    assert len(r.content) < len(r2.content)
    # 2. 使用 fake_useragent 随机 User-Agent
    r3 = requests.get(url, headers={'User-Agent': UserAgent().random})
    assert len(r.content) < len(r3.content)


class TestSelenium:
    """
    `selenium <https://pypi.org/project/selenium/>`_：自动化 web 浏览器交互
    """

    def test_selenium(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as ec
        options = webdriver.ChromeOptions()
        # 不显示图形界面
        # options.add_argument('headless')
        service = Service(executable_path='chromedriver.exe')
        driver = webdriver.Chrome(options=options, service=service)
        driver.get('https://www.baidu.com')

        print(driver.current_url)
        print(driver.title)
        # print(webdriver.page_source)
        # 截图
        driver.save_screenshot('baidu.png')
        os.remove('baidu.png')
        # region 搜索 selenium
        chat_textarea = driver.find_element(By.ID, 'chat-textarea')
        chat_textarea.send_keys('selenium')
        chat_submit_button = driver.find_element(By.ID, 'chat-submit-button')
        chat_submit_button.click()
        # 等待直到，某元素可见
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'page')))
        # endregion
        # 通过执行 js 滚动到底部
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)
        # 通过执行 js 打开一个窗口
        driver.execute_script('window.open("https://www.sogou.com")')
        # 所有窗口句柄
        handles = driver.window_handles
        # 切换窗口
        driver.switch_to.window(handles[1])
        time.sleep(1)
        # 关闭浏览器并关闭 ChromeDriver
        driver.quit()


class TestTenacity:
    """
    `tenacity <https://pypi.org/project/tenacity/>`_：多用途重试库
    """

    @staticmethod
    def do_something():
        if random.random() < 0.8:
            print("失败")
            raise Exception("异常")
        else:
            print("成功")

    @staticmethod
    def do_something2():
        if random.random() < 0.7:
            print("失败")
            return False
        else:
            print("成功")
            return True

    def test_stop(self):
        # stop_after_attempt：最多重试次数
        from tenacity import stop_after_delay, stop_never, stop_any, stop_all
        do_something = retry(stop=stop_after_attempt(10))(self.do_something)
        do_something()
        # stop_after_delay：最多重试总秒数
        do_something = retry(stop=stop_after_delay(10))(self.do_something)
        do_something()
        # stop_never：重试直到成功；不设置 stop，效果等同于 stop_never
        do_something = retry(stop=stop_never)(self.do_something)
        do_something()
        # stop_any
        do_something = retry(stop=stop_any(stop_after_attempt(5), stop_after_delay(5)))(self.do_something)
        do_something()
        # stop_all
        do_something = retry(stop=stop_all(stop_after_attempt(5), stop_after_delay(5)))(self.do_something)
        do_something()

    def test_wait(self):
        from tenacity import wait_fixed, wait_random, wait_exponential, wait_random_exponential, wait_none
        # wait_fixed：每次等待秒数
        do_something = retry(wait=wait_fixed(1))(self.do_something)
        do_something()
        # wait_random：每次等待随机秒数
        do_something = retry(wait=wait_random(1, 3))(self.do_something)
        do_something()
        # wait_exponential：指数退避，等待 multiplier*2^尝试次数，即依次等待 1 2 4 8 10 10 10 …
        do_something = retry(wait=wait_exponential(1, 10))(self.do_something)
        do_something()
        # wait_random_exponential：等待 random()*multiplier*2^尝试次数
        do_something = retry(wait=wait_random_exponential(2, 10))(self.do_something)
        do_something()
        # wait_none：不等待
        do_something = retry(wait=wait_none())(self.do_something)
        do_something()

    def test_retry(self):
        from tenacity import (retry_if_exception, retry_if_exception_type, retry_if_result, retry_if_exception_message,
                              retry_any, retry_all)
        # retry_if_exception_type：只对指定异常重试
        do_something = retry(retry=retry_if_exception_type(Exception))(self.do_something)
        do_something()
        # retry_if_exception：抛出异常时执行 predicate，返回 True 重试
        do_something = retry(retry=retry_if_exception(lambda e: type(e) is Exception))(self.do_something)
        do_something()
        # retry_if_result：有返回值时执行 predicate，返回 True 重试
        do_something = retry(retry=retry_if_result(lambda res: res is False))(self.do_something2)
        do_something()
        # retry_if_exception_message：根据异常消息是否包含指定字符串决定是否重试
        do_something = retry(retry=retry_if_exception_message(match="异常"))(self.do_something)
        do_something()
        # retry_any
        do_something = retry(
            retry=retry_any(retry_if_exception_type(Exception), retry_if_exception_message(match="异常"))
        )(self.do_something)
        do_something()
        # retry_all
        do_something = retry(
            retry=retry_all(retry_if_exception_type(Exception), retry_if_exception_message(match="异常"))
        )(self.do_something)
        do_something()

    def test_before_after(self):
        """
        before → 失败 → after → before_sleep → 等待 → …
        """
        from tenacity import before_sleep_log
        def log_before(retry_state):
            print(f"🟢 [before] 第{retry_state.attempt_number}次尝试")

        def log_after(retry_state):
            print(f"🔴 [after]  总耗时{retry_state.seconds_since_start}秒\n")

        do_something = retry(
            before=log_before, after=log_after, before_sleep=before_sleep_log(logging.getLogger(), logging.INFO)
        )(self.do_something)
        do_something()

    def test_raise(self):
        from tenacity import RetryError
        # reraise=False，抛出 RetryError；reraise=True，抛出原始异常
        do_something = retry(stop=stop_after_attempt(1), reraise=True)(self.do_something)
        try:
            do_something()
        except RetryError:
            print('RetryError')
        except Exception:
            print('Exception')


def test_jsonpath_ng():
    """
    `requests <https://pypi.org/project/jsonpath-ng/>`_
    """
    from jsonpath_ng import parse
    r = requests.get("https://reqres.in/api/users", headers={"x-api-key": "reqres-free-v1"})
    titles = [match.value for match in parse('$.data[*].first_name').find(r.json())]
    print(titles[:5])


def test_lxml():
    """
    `lxml <https://pypi.org/project/lxml/>`_：

    1. 通过封装 C 库（libxml2/libxslt）提供强大的 XML/HTML 处理能力
    2. 以 ElementTree API（xml.etree.ElementTree） 形式暴露给开发者，兼顾安全性与易用性
    3. 支持 XPath、RelaxNG、XML Schema、XSLT、C14N 等功能
    """
    from lxml import etree
    r = requests.get("https://www.w3schools.com/xml/books.xml")
    root = etree.XML(r.content)
    assert (root.xpath('/bookstore/book[2]/author/text()'), 'J K. Rowling')
    assert (root.xpath('/bookstore/book[2]/title/@lang/text()'), 'Harry Potter')


def test_moviepy():
    """
    `MoviePy <https://pypi.org/project/moviepy/>`_：用于视频编辑：剪切、连接、插入标题、视频合成（也称为非线性编辑）、视频处理和创建自定义效果
    """
    import tempfile
    from moviepy import AudioFileClip, VideoFileClip
    ua = UserAgent()

    def get_windows_ua():
        return next((ua.random for _ in range(10) if 'Windows' in ua.random),
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    url = 'https://www.bilibili.com/video/BV1D4411L7Qd/'
    headers = {'User-Agent': get_windows_ua(), 'Referer': url}
    r = requests.get(url, headers=headers)
    audio_url = re.search(r'"id":30216,"baseUrl":"(.*?)","base_url"', r.text).group(1)
    video_url = re.search(r'"id":16,"baseUrl":"(.*?)","base_url"', r.text).group(1)
    audio_data = requests.get(audio_url, headers=headers).content
    video_data = requests.get(video_url, headers=headers).content
    with (tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_audio,
          tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_video):
        temp_audio.write(audio_data)
        temp_video.write(video_data)
        temp_audio_path, temp_video_path = temp_audio.name, temp_video.name
    try:
        with AudioFileClip(temp_audio_path) as audio, VideoFileClip(temp_video_path) as video:
            video.with_audio(audio).write_videofile(
                'video.mp4',
                threads=os.cpu_count(),
                codec='libx264',
                audio_codec='aac',
                preset='fast',
                ffmpeg_params=['-movflags', '+faststart']
            )
    finally:
        os.remove(temp_audio_path) if os.path.exists(temp_audio_path) else None
        os.remove(temp_video_path) if os.path.exists(temp_video_path) else None


def test_pymysql():
    """
    `PyMySQL <https://pypi.org/project/PyMySQL/>`_
    """
    import pymysql
    from pymysql import cursors
    connection = pymysql.connect(host='43.136.102.115',
                                 user='root',
                                 password='Cesc123!',
                                 database='epitome',
                                 charset='utf8mb4',
                                 cursorclass=cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `demo` (`id`, `name`) VALUES (%s, %s)"
            cursor.execute(sql, ('1', 'ljh'))
        connection.commit()
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `name` FROM `demo` WHERE `id`=%s"
            cursor.execute(sql, 1)
            result = cursor.fetchone()
            print(result)
        with connection.cursor() as cursor:
            sql = "DELETE FROM `demo` WHERE id=%s"
            cursor.execute(sql, 1)
        connection.commit()


class TestOpenpyxl:
    """
    `openpyxl <https://pypi.org/project/openpyxl/>`_：用于读取/写入Excel 2010 xlsx/xlsm/xltx/xltm文件
    """
    import openpyxl

    def test_read(self):
        workbook = self.openpyxl.load_workbook("test.xlsx")
        # 工作表列表
        assert workbook.sheetnames == [sheet.title for sheet in workbook]
        # 工作表
        assert workbook.active == workbook[workbook.sheetnames[0]]
        worksheet = workbook.active
        # (行数，列数)
        assert (worksheet.max_row, worksheet.max_column) == (9, 3)
        # 工作表切片
        assert worksheet['A1:B2'] == ((worksheet['A1'], worksheet['B1']), (worksheet['A2'], worksheet['B2']))
        # 行切片
        assert worksheet['2:3'] == (worksheet[2], worksheet[3])
        # 列切片
        assert worksheet['C:D'] == (worksheet['C'], worksheet['D'])
        # 单元格
        assert worksheet['A'][0] == worksheet['A1'] == worksheet.cell(1, 1)
        # 遍历工作表
        for worksheet in workbook:
            # 遍历行
            for row in worksheet:
                assert isinstance(row, tuple)
                for cell in row:
                    print(cell.coordinate, cell.row, cell.column, cell.value)
            # 遍历行
            for row in worksheet.iter_rows(min_row=1, max_row=2, min_col=1, max_col=2): pass
            # 遍历列
            for column in worksheet.columns: pass
        # 十进制 ↔ 列字母
        from openpyxl.utils import get_column_letter, column_index_from_string
        assert (get_column_letter(100), column_index_from_string('CV')) == ('CV', 100)

    def test_write(self):
        from openpyxl.utils import get_column_letter
        workbook = self.openpyxl.load_workbook("test.xlsx")
        worksheet = workbook[workbook.sheetnames[1]]
        # 设置工作表标题
        worksheet.title = 'write'
        for _ in range(worksheet.max_row + 1):
            # 删除行
            worksheet.delete_rows(1)
        for row in range(1, 10):
            # 在工作表底部追加一行值
            worksheet.append([get_column_letter(col) + str(row) for col in range(1, 10)])
        for col in range(1, 10):
            row = 10
            # 设置单元格
            worksheet.cell(row, col, get_column_letter(col) + str(row))
        # 删除工作表
        workbook.remove(workbook[workbook.sheetnames[2]])
        # 创建工作表
        workbook.create_sheet('new', 2)
        # 保存当前工作簿
        workbook.save('test.xlsx')
