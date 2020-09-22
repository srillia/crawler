# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import copy

from itemadapter import ItemAdapter

from lib import mongo_lib, common


class UnsunPipeline:
    def process_item(self, item, spider):
        # birth = item["birth"]
        # if common.is_gt_now_date(birth):
        # 去重复
        criteria = dict(item)
        del criteria['date']
        result = mongo_lib.find_one(criteria)
        if result is None:
            mongo_lib.insert_one(dict(item))
        return item
