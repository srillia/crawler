# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EduInfoItem(scrapy.Item):
    origin = scrapy.Field()
    column = scrapy.Field()
    title = scrapy.Field()
    birth = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    # 来源
    from_origin = scrapy.Field()
    # 内容
    content = scrapy.Field()

# 广西教育厅
class GxjytInfoItem(scrapy.Item):
    # 广西壮族自治区教育厅
    origin = scrapy.Field()
    # 教育要闻
    column = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 日期
    birth = scrapy.Field()
    # 地址
    link = scrapy.Field()
    # 详细时间
    date = scrapy.Field()
    # 来源
    from_origin = scrapy.Field()
    # 内容
    content = scrapy.Field()


class CNHvcEdu(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    intro = scrapy.Field()
    origin = scrapy.Field()
    birth = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    column = scrapy.Field()
    source = scrapy.Field()
    page = scrapy.Field()


class BGzjInfoItem(scrapy.Item):
    # 来源
    origin = scrapy.Field()
    # 项目
    column = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 文章发布时间
    birth = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 爬取时间
    date = scrapy.Field()
    # 文章来源
    source = scrapy.Field()
    # 文章内容
    content =scrapy.Field()
    # 文章作者
    author = scrapy.Field()