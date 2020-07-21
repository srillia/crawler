from threading import Timer
from datetime import datetime


class MyTimer(object):

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


class AA:
    def hello(self, name, age):
        print("[%s]\thello %s: %d\n" % (datetime.now().strftime("%Y%m%d %H:%M:%S"), name, age))


if __name__ == "__main__":
    aa = AA()
    start = datetime.now()
    tmr = MyTimer(start, 5, aa.hello, ["owenliu", 18])
    tmr.start()
    # tmr.cancel()