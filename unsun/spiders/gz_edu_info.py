import time
import scrapy
from scrapy import Request

from lib import common
from unsun.items import CommonItem


class GzEduInfoSpider(scrapy.Spider):
    name = 'gz_edu_info'
    allowed_domains = ['edu.gd.gov.cn']
    # start_urls = ['http://edu.gd.gov.cn/zxzx/index.html']

    def __init__(self, oderurl=None, origin_id=None, *args, **kwargs):
        super(GzEduInfoSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['%s' % oderurl]
        self.origin_id = '%s' % origin_id

    def parse(self, response):
        origin = "广东省教育厅"
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
                edu_info_item = CommonItem()
                edu_info_item["origin"] = origin
                edu_info_item["column"] = column
                edu_info_item["title"] = title
                edu_info_item["link"] = link
                edu_info_item["birth"] = birth
                edu_info_item["date"] = date
                yield Request(url=link, meta={"item": edu_info_item}, callback=self.parse_content)
        if next_url is not None:
            # 继续爬取分类分页的其它页面
            yield scrapy.Request(next_url)

    def parse_content(self, response):
        content = response.xpath("//div[@id='zoom']/div[@id='zoomcon']").extract_first()
        item = response.meta['item']
        item["content"] = content
        yield item
