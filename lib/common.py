import datetime
import os
import sys
import time

from threading import Timer
from datetime import datetime


class UnsunTimer(object):

    def __init__(self, start_time, interval, callback_proc, args=None, kwargs=None):
        self.__timer = None
        self.__start_time = start_time
        self.__interval = interval
        self.__callback_pro = callback_proc
        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}

    def exec_callback(self, args=None, kwargs=None):
        self.__callback_pro(*self.__args, **self.__kwargs)
        self.__timer = Timer(self.__interval, self.exec_callback)
        self.__timer.start()

    def start(self):
        interval = self.__interval - (datetime.now().timestamp() - self.__start_time.timestamp())
        print(interval)
        self.__timer = Timer(interval, self.exec_callback)
        self.__timer.start()

    def cancel(self):
        self.__timer.cancel()
        self.__timer = None


class PathUtil(object):
    """路径处理工具类"""
    def __init__(self):
        # 判断调试模式
        debug_vars = dict((a, b) for a, b in os.environ.items()
                          if a.find('IPYTHONENABLE') >= 0)
        # 根据不同场景获取根目录
        if len(debug_vars) > 0:
            """当前为debug运行时"""
            self.rootPath = sys.path[2]
        elif getattr(sys, 'frozen', False):
            """当前为exe运行时"""
            self.rootPath = os.getcwd()
        else:
            """正常执行"""
            self.rootPath = sys.path[1]
        # 替换斜杠
        self.rootPath = self.rootPath.replace("\\", "/")

    def get_path_from_resources(self, file_name):
        """按照文件名拼接资源文件路径"""
        file_path = "%s/resources/%s" % (self.rootPath, file_name)
        return file_path


# 将日期字符串转为时间再比较，time，datetime,str
def is_gt_now_date(timestr):
    # 获取当前时间日期
    nowTime_str = datetime.datetime.now().strftime('%Y-%m-%d')
    print(nowTime_str)
    # mktime参数为struc_time,将日期转化为秒，
    e_time = time.mktime(time.strptime(nowTime_str, "%Y-%m-%d"))
    print(e_time)
    try:
        s_time = time.mktime(time.strptime(timestr, '%Y-%m-%d'))
        print(s_time)
        # 日期转化为int比较
        diff = int(s_time) - int(e_time)
        print(diff)
        if diff >= 0:
            return True
        else:
            print('所查日期不能小于当前时间！！！')
            return False
    except Exception as e:
        print(e)
        return False


def save_to_file(name, text):
    pathUtil = PathUtil()
    file = open(pathUtil.rootPath + "/tmp/" + name, 'w', encoding='utf-8')
    file.write(text)
    file.close()


