import time

import scrapy
from scrapy_splash import SplashRequest

from lib import common
from unsun.items import GxjytInfoItem



# 广西壮族自治区教育厅网站
class GxjytSpider(scrapy.Spider):
    name = 'gxjyt_jyyw_info'
    allowed_domains = ['jyt.gxzf.gov.cn']
    start_urls = ['http://jyt.gxzf.gov.cn/jyxw/jyyw/']

    # 开始页面 初始化page参数为1
    def start_requests(self):
        for url in self.start_urls:
            # 开始
            yield SplashRequest(url, callback=self.parse)

    def parse(self, response):
        # 保存下载html文件
        common.save_to_file("gxjyt_jyyw_info.html", response.text)
        items = response.xpath("//ul[@class='more-list']//li")
        for item in items:
            link = "http://jyt.gxzf.gov.cn/jyxw/jyyw" + item.xpath("./a/@href").extract_first().replace(".", "", 1)
            yield SplashRequest(link, callback=self.parse_context)

        next_url = "http://jyt.gxzf.gov.cn/jyxw/jyyw/" + response.xpath(
            "//div[@class='more-page']/a[last()]/@href").extract_first()
        next_page = response.urljoin(next_url)
        if next_url is not None:
            # 继续爬取分类分页的其它页面
            try:
                yield SplashRequest(next_page)
            except:
                pass

    def parse_context(self, response):
        content_select = response.xpath(
            "//div[@class='view TRS_UEDITOR trs_paper_default trs_web'] "
            "| //div[@class='view TRS_UEDITOR trs_paper_default trs_web trs_key4format']"
            "| //div[@class='view TRS_UEDITOR trs_paper_default trs_web trs_word trs_key4format']"
            "| //div[@class='view TRS_UEDITOR trs_paper_default trs_word']"
            "| //div[@class='view TRS_UEDITOR trs_paper_default']"
            "| //div[@class='view TRS_UEDITOR trs_paper_default trs_web trs_word']"
            "| //div[@class='view TRS_UEDITOR trs_paper_default trs_word trs_key4format']"
        )
        content = content_select.extract_first()
        img_list = content_select.xpath("//img/@src").extract()
        if len(img_list) > 0:
            for img in img_list:
                new_img = "http://jyt.gxzf.gov.cn/jyxw/jyyw/" + img.replace(".", "", 1)
                content = content.replace(img, new_img)
        title = response.xpath("//div[@class='article']/h1/text()").extract_first()
        origin_and_birth = response.xpath(
            "//div[@class='article-inf-left']/text()").extract_first().lstrip().rstrip().split("\n", 1)
        link = response.xpath("//meta[@name='Url']/@content").extract_first()
        origin = "广西壮族自治区教育厅"
        column = "教育要闻"
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        birth = origin_and_birth[0]
        from_origin = "广西壮族自治区教育厅"
        if len(origin_and_birth) > 1:
            from_origin = origin_and_birth[1].lstrip().replace("来源：", "")
        gxjyt_info_item = GxjytInfoItem()
        gxjyt_info_item["origin"] = origin
        gxjyt_info_item["column"] = column
        gxjyt_info_item["title"] = title
        gxjyt_info_item["link"] = link
        gxjyt_info_item["birth"] = birth
        gxjyt_info_item["date"] = date
        gxjyt_info_item["from_origin"] = from_origin
        gxjyt_info_item["content"] = content
        yield gxjyt_info_item