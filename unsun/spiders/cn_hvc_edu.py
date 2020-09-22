import logging
import time

import scrapy

from unsun.items import CommonItem


class CNHvcEduSpider(scrapy.Spider):
    name = 'CNHvcEdu'
    allowed_domains = ['tech.net.cn']
    start_urls = ['http://www.tech.net.cn/news/list/100.html','http://www.tech.net.cn/news/list/101.html','http://www.tech.net.cn/news/list/102.html']
    ## 数据源id
    origin_id = 0

    def __init__(self, oderurl=None,origin_id=None, *args, **kwargs):
        super(CNHvcEduSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['%s' % oderurl]
        self.origin_id = '%s' % origin_id


    def parse(self, response):
        # print("---------------------------------------------------------------------------------------")
        # newsName = response.xpath("//div[@class='title trim']/a").xpath('string(.)').extract()
        # print(newsName)
        # list =[]
        p = "http://www.tech.net.cn"
        str(self).encode("utf-8")

        # 列表页
        news_urls = response.xpath("//h4/a/@href")
        nest_page_url = response.xpath("//div[@class='digg']/a[last()]/@href").extract_first()
        title = response.xpath("//h1[@class='m-t-10 m-b-5']/text()").extract_first()

        i = 0
        # print(news_urls)
        if len(news_urls) != 0 and title is None:
            for url in news_urls:
                page = response.xpath("//div[@class='page-box']/div[@class='digg']/span[@class='current']/text()").extract_first()
                link = p + url.extract()
                i = i + 1
                # print("link", i, ":", link)
                news_info = CommonItem()
                news_info["link"] = link
                news_info["dataOriginId"] = self.origin_id
                yield scrapy.Request(news_info["link"], meta={"news_info": news_info})
                # time.sleep(1)

            # 翻页
            # print("翻页", p + nest_page_url)
            if nest_page_url is not None:
                yield scrapy.Request(url=p + nest_page_url)
        else:
            title = response.xpath("//h1[@class='m-t-10 m-b-5']/text()").extract_first()
            if title is not None and len(title) > 0:
                content = response.xpath("//div[@class='contentabnc']/section").extract_first()
                date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                birth = response.xpath("//div[@class='info font-weight-300']/span[1]/text()").extract_first()
                if birth is not None:
                    birth = birth.split('：')[-1]
                column = response.xpath("//ol/li[@class='breadcrumb-item']/text()").extract()[-1]
                if column is not None:
                    column = column.split('> ')[-1]
                # print("----------------------", column)
                intro = response.xpath("//h4/text()").extract_first()
                source = response.xpath("//div[@class='info font-weight-300']/span[4]/text()").extract_first()
                if source is not None:
                    source = source.split(': ')[-1]
                # print("----------------------", birth)
                news_info = response.meta["news_info"]
                news_info["content"] = content
                news_info["date"] = date
                news_info["birth"] = birth
                news_info["intro"] = intro
                news_info["organ"] = source
                news_info["origin"] = "中国高职高专网"
                news_info["title"] = title
                news_info["column"] = column
                # print("info", news_info)
                yield news_info
        pass


class CNHvcEduSpider_reform(scrapy.Spider):
    name = 'CNHvcEdu_reform'
    allowed_domains = ['tech.net.cn']
    start_urls = ['https://www.tech.net.cn/news/88.html']
    ## 数据源id
    origin_id = 0

    def __init__(self, oderurl=None,origin_id=None, *args, **kwargs):
        super(CNHvcEduSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['%s' % oderurl]
        self.origin_id = '%s' % origin_id

    def parse(self, response):
        # print("---------------------------------------------------------------------------------------")
        # newsName = response.xpath("//div[@class='title trim']/a").xpath('string(.)').extract()
        # print(newsName)
        # list =[]
        p = "http://www.tech.net.cn"

        # 列表页
        news_urls = response.xpath("//h4/a/@href")
        nest_page_url = response.xpath("//div[@class='digg']/a[last()]/@href").extract_first()
        title = response.xpath("//h1[@class='m-t-10 m-b-5']/text()").extract_first()

        i = 0
        # print(news_urls)
        if len(news_urls) != 0 and title is None:
            for url in news_urls:
                page = response.xpath("//div[@class='page-box']/div[@class='digg']/span[@class='current']/text()").extract_first()
                link = p + url.extract()
                i = i + 1
                # print("link", i, ":", link)
                news_info = CommonItem()
                news_info["link"] = link
                news_info["dataOriginId"] = self.origin_id
                yield scrapy.Request(news_info["link"], meta={"news_info": news_info})
                # time.sleep(1)

            # 翻页
            # print("翻页", p + nest_page_url)
            if nest_page_url is not None:
                yield scrapy.Request(url=p + nest_page_url)
        else:
            title = response.xpath("//h1[@class='m-t-10 m-b-5']/text()").extract_first()
            if title is not None and len(title) > 0:
                content = response.xpath("//div[@class='contentabnc']/section").extract_first()
                date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                birth = response.xpath("//div[@class='info font-weight-300']/span[1]/text()").extract_first()
                if birth is not None:
                    birth = birth.split('：')[-1]
                column = "教学改革"
                # print("----------------------", column)
                intro = response.xpath("//h4/text()").extract_first()
                source = response.xpath("//div[@class='info font-weight-300']/span[4]/text()").extract_first()
                if source is not None:
                    source = source.split(': ')[-1]
                # print("----------------------", birth)
                news_info = response.meta["news_info"]
                news_info["content"] = content
                news_info["date"] = date
                news_info["birth"] = birth
                news_info["intro"] = intro
                news_info["source"] = source
                news_info["origin"] = "中国高职高专网"
                news_info["title"] = title
                news_info["column"] = column
                # print("info", news_info)
                yield news_info
        pass

