import os

from lib import mongo_lib
# from unsun.items import TokeyItem
#
# tokey_item = TokeyItem()
# tokey_item["origin"] = "test"

# mongo_lib.insert_one(dict(tokey_item))


# import datetime
# import time
# #将日期字符串转为时间再比较，time，datetime,str
# def valid_date(timestr):
#     #获取当前时间日期
#     nowTime_str = datetime.datetime.now().strftime('%Y-%m-%d')
#     print(nowTime_str)
#     #mktime参数为struc_time,将日期转化为秒，
#     e_time = time.mktime(time.strptime(nowTime_str,"%Y-%m-%d"))
#     print(e_time)
#     try:
#         s_time = time.mktime(time.strptime(timestr, '%Y-%m-%d'))
#         print(s_time)
#         #日期转化为int比较
#         diff = int(s_time)-int(e_time)
#         print(diff)
#         if diff >= 0:
#             return 1
#         else:
#             print('所查日期不能小于当前时间！！！')
#             return 0
#     except Exception as e:
#         print(e)
#         return 0
# if __name__=='__main__':
#     valid_date("2020-7-14")

import sys
import os


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

    def get_path_from_resources(self, fileName):
        """按照文件名拼接资源文件路径"""
        file_path = "%s/resources/%s" % (self.rootPath, fileName)
        return file_path


path_util = PathUtil()

if __name__ == '__main__':
    """测试"""
    # path = PathUtil.getPathFromResources("context.ini")
    print(path_util.rootPath)
