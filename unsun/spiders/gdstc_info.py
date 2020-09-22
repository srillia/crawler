import scrapy
import time
from unsun.items import CommonItem


# 广东省科技厅
class GDSTCSpider(scrapy.Spider):
    name = "gdstc"
    allowed_domains = ["gdstc.gd.gov.cn"]
    start_urls = [
        "http://gdstc.gd.gov.cn/zwgk_n/zcfg/zcjd/index.html",
        "http://gdstc.gd.gov.cn/zwgk_n/zcfg/szcfg/index.html",
        "http://gdstc.gd.gov.cn/zwgk_n/zcfg/gjzc/index.html",
        "http://gdstc.gd.gov.cn/zwgk_n/tzgg/index.html",
    ]
    origin_id = 0

    # 新增初始化方法
    def __init__(self, oderurl=None, origin_id=None, *args, **kwargs):
        super(GDSTCSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['%s' % oderurl]
        self.origin_id = '%s' % origin_id

    def parse(self, response):
        item = CommonItem()
        detail_url = response.xpath("//div[@class='newsList right']/ul[@class='list']/li/a/@href").extract()
        next_url = response.xpath("//div[@class='page']/a[@class='next']/@href").extract_first()
        for i in range(len(detail_url)):
            path_url = "//div[@class='newsList right']/ul[@class='list']/li" + "[" + str(i + 1) + "]" + "/a/@href"
            reality_url = response.xpath(path_url).extract_first()
            yield scrapy.Request(reality_url, meta={'item': item, 'url': reality_url}, callback=self.parse2)
        yield scrapy.Request(next_url)

    def parse2(self, response):
        item = response.meta['item']

        # 新增数据源id
        item['dataOriginId'] = self.origin_id

        item['link'] = response.meta['url']
        date = response.xpath("//div[@class='zw-info']/span[@class='time']/text()").extract_first()
        organ = response.xpath(
            "//div[@class='viewList']/div[@class='zw-info']/span[@class='ly']/text()").extract_first()
        if organ is not None:
            item['organ'] = organ[7:]
        item['title'] = response.xpath("//div[@class='viewList']/h3[@class='zw-title']/text()").extract_first()
        item['birth'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if date is not None:
            item['date'] = date[7:26]
        item['column'] = response.xpath("//div[@class='pos']/a[last()]/text()").extract_first()
        item['origin'] = "广东省科技厅"
        item['content'] = response.xpath("//div[@class='viewList']/div[@class='zw']").extract()
        item['column'] = response.xpath("//div[@class='pos']/a[last()]/text()").extract_first()
        yield item