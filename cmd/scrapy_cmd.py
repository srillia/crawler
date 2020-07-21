from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import time
import logging
from scrapy.utils.project import get_project_settings

# 在控制台打印日志
configure_logging()
# CrawlerRunner获取settings.py里的设置信息
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl():
    while True:
        logging.info("new cycle starting")
        #yield runner.crawl("edu_info")
        yield runner.crawl("gfjyb_edu_info")
        # 1s跑一次
        time.sleep(5)
    reactor.stop()


crawl()
reactor.run()