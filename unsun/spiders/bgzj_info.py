
# 八桂职教
from datetime import time

import scrapy
from scrapy_splash import SplashRequest

from lib.common import save_to_file
from unsun.items import CommonItem
from unsun.spiders.cn_hvc_edu import CNHvcEduSpider


class BGzjSpider(scrapy.Spider):
    name = 'bgzj_edu_info'
    allowed_domains = ['ep12.com']
    start_urls = ['http://www.ep12.com/a/xinwen/dongtai', 'http://www.ep12.com/a/xinwen/yaowen']

    # 开始页面 初始化page参数为1
    def start_requests(self):
        for url in self.start_urls:
            # 开始
            yield SplashRequest(url, callback=self.parse)


    def parse(self, response):
        origin = "广西八桂职教"
        print(origin)
        # 保存下载html文件
        save_to_file("gfjyb_edu_info.html", response.text)

        next_url = response.xpath(
            "//div[@class='d-h d-h-content']/div[@class='container clearfix']/div[@class='search_fl_Content']/div[@id='d_pagination']/a[@class='next']/@href").extract_first()
        next_page = response.urljoin(next_url)

        items = response.xpath(
            "//div[@class='d-h d-h-content']/div[@class='container clearfix']/div[@class='search_fl_Content']/div[@class='top-10']/div[@class='title trim']")
        bgzi_info_item = CommonItem()
        bgzi_info_item['origin'] = origin
        bgzi_info_item['birth'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # for detail in detail_url:
        #     if detail is not None:
        #         yield SplashRequest(detail, callback=self.parse)
        for item in items:
            link = item.xpath("./a/@href").extract_first()
            if link is not None:
                bgzi_info_item['link'] = link
                print(link)
                yield SplashRequest(link, meta={"item": bgzi_info_item}, callback=self.parse_content)

        # for item in items:
        #     title = item.xpath("./div[@class='title trim']/a/text()|./div[@class='title trim']/a/b/text()").extract_first()
        #     link = item.xpath("./div[@class='title trim']/a/@href").extract_first()
        #     # 栏目与生产日期
        #     messages = item.xpath("./div[@class='info']/text()").extract_first().split("&nbsp&nbsp&nbsp")
        #     column = messages[0].replace('栏目:','')
        #     birth = messages[2].replace('日期:','')
        #     date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #     edu_info_item = BGzjInfoItem()
        #     edu_info_item["origin"] = origin
        #     edu_info_item["column"] = column
        #     edu_info_item["title"] = title
        #     edu_info_item["link"] = link
        #     edu_info_item["birth"] = birth
        #     edu_info_item["date"] = date
        #     yield edu_info_item

        if next_url is not None:
            # 继续爬取分类分页的其它页面
            try:
                yield SplashRequest(next_page)
            except:
                pass

    def parse_content(self, response):
        item = CommonItem()
        item['link'] = response.url
        # 详情内容页面链接
        # 标题
        detail_title = response.xpath(
            "//div[@class='container clearfix']/div[@class='search_fl_Content']/div[@class='fTitle']/text()").extract_first()
        detail_url = response.xpath(
            "//div[@class='search_fl_Content']/div[@class='top-10'] /div[@class='title trim']/a/@href")
        # 数据来源 栏目
        detail_column = response.xpath(
            "//div[@class='container clearfix']/div[@class='search_fl_Content']/div[@class='top-10']/div[@class='fPost']/a[3]/text()").extract_first()
        # 部分页面html不一样
        other_detail_column = response.xpath(
            "//div[@class='container clearfix']/div[@class='search_fl_Content']/div[@class='top-10']/div[@class='fPost']/a/text()").extract_first()
        # 发文机构
        detail_organ = response.xpath(
            "//div[@class='container clearfix']/div[@class='search_fl_Content']/div[@class='flai']/span[1]/text()").extract_first()
        # 发文作者
        detail_author = response.xpath(
            "//div[@class='container clearfix']/div[@class='search_fl_Content']/div[@class='flai']/span[2]/text()").extract_first()
        # 发文时间
        detail_birth = response.xpath(
            "//div[@class='container clearfix']/div[@class='search_fl_Content']/div[@class='flai']/span[3]/text()").extract_first()
        # 文章内容
        detail_content = response.xpath(
            "//div[@class='container clearfix']/div[@class='search_fl_Content']/div[@class='fcontent']/div[@class='contentBoxF']/p|//div[@class='container clearfix']/div[@class='search_fl_Content']/div[@class='fcontent']/div[@class='contentBoxF']/div")

        item['title'] = detail_title
        # print(bgzi_info_item)
        if detail_column is not None:
         item ['column'] = detail_column
        else :
            item['column'] =other_detail_column
        # print(bgzi_info_item)
        # if detail_source is not None:
        item['organ'] = detail_organ
        # print(bgzi_info_item)
        item["dataOriginId"] = self.origin_id
        # if detail_author is not None:
        item['author'] = detail_author
        # print(bgzi_info_item)
        # if detail_birth is not None:
        item['birth'] = detail_birth
        # print(bgzi_info_item)
        # if detail_content is not None:
        detail_content_str = ""
        # 图片路径相对路径转换为绝对路径
        for content in detail_content:
            old_src = content.xpath("./img/@src |./strong/img/@src ").extract_first()
            if old_src is not None:
                new_src = response.urljoin(old_src)
                detail_content_str = detail_content_str + content.extract().replace(old_src, new_src)

            else:
                detail_content_str = detail_content_str + content.extract()

        item['content'] = detail_content_str
        item['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # fo = open("rawcodes.txt", "wb")
        # fo.write((item, -1))
        #
        # # 关闭打开的文件
        # fo.close()
        yield item

 ## 数据源id
    origin_id = 0

    def __init__(self, oderurl=None,origin_id=None, *args, **kwargs):
        super(CNHvcEduSpider, self).__init__(*args, **kwargs)
        #将传入的url赋值给start_urls
        self.start_urls = ['%s' % oderurl]
        #将数据源id赋值给origin_id
        self.origin_id = '%s' % origin_id