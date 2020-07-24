from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

host = settings["MONGO_HOST"]
port = settings["MONGO_PORT"]
account = settings["MONGO_ACCOUNT"]
password = settings["MONGO_PASSWORD"]

conn = MongoClient("mongodb://" + account + ":" + password + "@" + host + ":" + str(port) + "/")

db = conn['spider']
edu = db["cn_hvc_edu"]


# 定义一个函数
def insert_one(data):
    print("-------------------------------------",conn)
    print("-------------------------------------",db)
    edu.insert_one(data)


# 定义一个函数
def find_one(data):
    return edu.find_one(data)
