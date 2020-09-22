# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# todo 尽量保证item一致，存在一个库当中
# 主键 id
# 数据来源平台 origin
# 数据开源平台的栏目 column
# 标题 title
# 发文日期  date
# 获取时间  birth
# 正文  content
# 发文机构 organ
# 作者  author
# 简介  intro
# 发文字号 newsNumber
# 来源链接 link
# 数据源id   dataOriginId
import scrapy


# 通用爬虫item
class CommonItem(scrapy.Item):
    #数据来源平台
    origin = scrapy.Field()
    # 数据开源平台的栏目
    column = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 获取时间
    birth = scrapy.Field()
    # 发文日期
    date = scrapy.Field()
    # 来源链接
    link = scrapy.Field()
    # 正文
    content = scrapy.Field()
    # 发文机构
    organ = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 简介
    intro = scrapy.Field()
    # 发文字号
    newsNumber = scrapy.Field()
    # 数据源id
    dataOriginId = scrapy.Field()


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
    organ = scrapy.Field()
    dataOriginId = scrapy.Field()


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
    content = scrapy.Field()
    # 文章作者
    author = scrapy.Field()
