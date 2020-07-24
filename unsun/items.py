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