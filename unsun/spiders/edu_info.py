import time

import scrapy
from scrapy_splash import SplashRequest

from lib import common
from unsun.items import EduInfoItem
from unsun.items import GxjytInfoItem


class EduInfoSpider(scrapy.Spider):
    name = 'edu_info'
    allowed_domains = ['edu.gd.gov.cn']
    start_urls = ['http://edu.gd.gov.cn/zxzx/index.html']

    def parse(self, response):

        origin = "广东省教育厅"
        print(origin)
        # 保存下载html文件
        common.save_to_file("edu_info.html", response.text)

        # 爬取资讯首页，获取urls信息
        urls = response.xpath("//div[@class='indexbox']//div[contains(@class,'ggjy_title')]//tr/td[2]/a/@href")
        if len(urls) != 0:
            for url in urls:
                # 继续爬取分类页面
                yield scrapy.Request(url.extract())
        # 如果不是资讯首页，则是资讯下面的分类
        else:
            next_url = response.xpath("//div[@class='page']/a[@class='next']/@href").extract_first()

            column = response.xpath("//div[@class='listright_title']//td[@class='lmbt_td']/span/text()").extract_first()
            items = response.xpath("//div[@class='main_cen']//div[@class='list_list']/ul/li[@class='list_li']")

            for item in items:
                title = item.xpath("./a/text()").extract_first()
                link = item.xpath("./a/@href").extract_first()
                birth = item.xpath("./span/text()").extract_first()
                date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                edu_info_item = EduInfoItem()
                edu_info_item["origin"] = origin
                edu_info_item["column"] = column
                edu_info_item["title"] = title
                edu_info_item["link"] = link
                edu_info_item["birth"] = birth
                edu_info_item["date"] = date
                yield edu_info_item

            if next_url is not None:
                # 继续爬取分类分页的其它页面
                yield scrapy.Request(next_url)


# 国防教育 spider
class GfjybSpider(scrapy.Spider):
    name = 'gfjyb_edu_info'
    allowed_domains = ['www.moe.gov.cn']
    start_urls = ['http://www.moe.gov.cn/jyb_sy/sy_jyyw/']

    # 开始页面 初始化page参数为1
    def start_requests(self):
        for url in self.start_urls:
            # 开始
            yield SplashRequest(url, callback=self.parse)

    def parse(self, response):

        origin = "中华人民共和国教育部"
        print(origin)
        # 保存下载html文件
        common.save_to_file("gfjyb_edu_info.html", response.text)
        next_url = response.xpath(
            "//div[@class='scy_tylb_fy-nr']//li[@class='m_page_a m_page_btn'][2]/a/@href").extract_first()
        next_page = response.urljoin(next_url)
        column = "教育要闻"
        items = response.xpath("//div[@id='wcmpagehtml']//ul[@id='list']/li")

        for item in items:
            title = item.xpath("./a/text()").extract_first()
            link = item.xpath("./a/@href").extract_first()
            birth = item.xpath("./span/text()").extract_first()
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            edu_info_item = EduInfoItem()
            edu_info_item["origin"] = origin
            edu_info_item["column"] = column
            edu_info_item["title"] = title
            edu_info_item["link"] = link
            edu_info_item["birth"] = birth
            edu_info_item["date"] = date
            yield edu_info_item

        if next_url is not None:
            # 继续爬取分类分页的其它页面
            try:
                yield SplashRequest(next_page)
            except:
                pass
