from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import time
import logging
from scrapy.utils.project import get_project_settings
from cmd.sql_cmd import MysqlDB

# 在控制台打印日志
configure_logging()
# CrawlerRunner获取settings.py里的设置信息
runner = CrawlerRunner(get_project_settings())

# todo 每个spoder中加
# def __init__(self, oderurl=None, origin_id=None, *args, **kwargs):
#     super(CNHvcEduSpider, self).__init__(*args, **kwargs)
#     self.start_urls = ['%s' % oderurl]
#     self.origin_id = '%s' % origin_id

@defer.inlineCallbacks
def crawl():
    # while True:
    #     # logging.info("new cycle starting")
    #     # #yield runner.crawl("edu_info")
    #     # yield runner.crawl("gfjyb_edu_info")
    #     # 查询启用状态的数据源
    #     results = MysqlDB.querystart(0)
    #     for row in results:
    #         origin_id = row[0]
    #         scrapy_name = row[1]
    #         url = row[2]
    #         # 打印结果
    #         logging.info("origin_id=%s,scrapy_name=%s,url=%s" % \
    #                      (origin_id, scrapy_name, url))
    #         logging.info("new cycle starting")
    #         #origin_id 数据源id, scrapy_name 爬虫脚本名称, url 爬虫地址url
    #         yield runner.crawl(crawler_or_spidercls=scrapy_name, oderurl=url, origin_id=origin_id)
    #
    #      # 1s跑一次
    #     time.sleep(5)
    # reactor.stop()


    results = MysqlDB.querystart(0)
    for row in results:
        origin_id = row[0]
        scrapy_name = row[1]
        url = row[2]
        # 打印结果
        logging.info("origin_id=%s,scrapy_name=%s,url=%s" % \
                     (origin_id, scrapy_name, url))
        logging.info("new cycle starting")
        # origin_id 数据源id, scrapy_name 爬虫脚本名称, url 爬虫地址url
        yield runner.crawl(crawler_or_spidercls=scrapy_name, oderurl=url, origin_id=origin_id)


crawl()
reactor.run()