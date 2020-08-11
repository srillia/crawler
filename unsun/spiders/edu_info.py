import time
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest

from lib import common
from unsun.items import EduInfoItem


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
    allowed_domains = ['www.moe.gov.cn', 'mp.weixin.qq.com', 'www.scio.gov.cn', 'politics.people.com.cn',
                       'paper.people.com.cn', 'www.china.com.cn']
    start_urls = ['http://www.moe.gov.cn/jyb_sy/sy_jyyw/']

    # start_urls = ['http://www.moe.gov.cn/jyb_sy/sy_jyyw/index_24.html']

    # 开始页面 初始化page参数为1
    def start_requests(self):
        for url in self.start_urls:
            # 开始
            yield SplashRequest(url, callback=self.parse)

    def parse(self, response):
        origin = "中华人民共和国教育部"
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
            if link.startswith("http:", 0, len(link) - 1) or link.startswith("https:", 0, len(link) - 1):
                edu_info_item["link"] = link
            else:
                http_link = "http://www.moe.gov.cn/" + link.replace("../../", "")
                edu_info_item["link"] = http_link
            edu_info_item["birth"] = birth
            edu_info_item["date"] = date
            yield Request(url=edu_info_item["link"], meta={"item": edu_info_item}, callback=self.parse_content)
        if next_url is not None:
            # 继续爬取分类分页的其它页面
            if next_url.startswith("javascript", 0, len(next_url) - 1):
                page_info = response.xpath(
                    "//div[@class='scy_tylb_fy-nr']//li[@class='m_page_a m_page_btn'][2]/a/@onclick").extract_first()
                page = page_info.replace("getWasRecord(", "").replace(");", "").split(",")
                url = "http://www.moe.gov.cn/was5/web/search?channelid=" + page[1] + "&chnlid=" + page[
                    0] + "&page="
                page_num = int(page[2])
                yield Request(url=(url + page[2]), meta={"next_page": (page_num + 1), "url": url},
                              callback=self.parse_next_page)
            else:
                try:
                    yield SplashRequest(next_page)
                except:
                    pass

    '''
    从25页后，分页的样式不一样，单独进行页面解析
    '''

    def parse_next_page(self, response):
        origin = "中华人民共和国教育部"
        column = "教育要闻"
        result_list = response.xpath("//li")
        for item in result_list:
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
            yield Request(url=edu_info_item["link"], meta={"item": edu_info_item}, callback=self.parse_content)
        next_page = response.meta['next_page']
        url = response.meta['url']
        print(type(next_page))
        page_num = int(next_page)

        if item is not None and url is not None:
            yield Request(url=(url + next_page), meta={"next_page": (page_num + 1), "url": url},
                          callback=self.parse_next_page)

    '''
    处理详情页，暂时未处理格式不一样的数据

    '''

    def parse_content(self, response):
        content = response.xpath("//div[@id='content_body']")
        item = response.meta['item']
        if len(content) != 0:
            context = content.xpath("./div[@class='TRS_Editor']").extract()
            source = response.xpath("//div[@id='content_date_source']/text()").extract_first()
            if source is not None:
                item["from_origin"] = source.strip().split("来源：")[1]
            item["content"] = context[0]
            yield item
        else:
            yield item
