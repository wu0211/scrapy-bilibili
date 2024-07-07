# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os
import requests

class ProxyPipeline:
    def isCurSpider(self, spider):
        return spider.name == 'proxy_spider'
    
    def open_spider(self, spider):
        if self.isCurSpider(spider):
            self.file = open('proxies.txt', 'w')

    def close_spider(self, spider):
        if self.isCurSpider(spider):
            self.file.close()

    def is_proxy_working(self, proxy):
        try:
            response = requests.get('https://www.bilibili.com/', proxies={ 'https': proxy}, timeout=5)
           
            return response.status_code == 200
        except Exception as e:
            print(e)
            return False

    def process_item(self, item, spider):
        
        if self.isCurSpider(spider):
            # print(item)
            proxy = item.get('proxy')
            # print(proxy)
            if proxy and self.is_proxy_working(proxy):
                self.file.write(f"{proxy}\n")
            return item
        
        return item


class BilibiliPipeline:
    data=[]
    def __init__(self) -> None:
        pass

    def isBilibili(self, spider):
        return spider.name == 'b'

    
    def open_spider(self, spider):
        if self.isBilibili(spider):
            self.file_name = 'bilibili.json'
            if not os.path.exists(self.file_name):
                self.data = []
            else:
                with open(self.file_name, 'r', encoding='utf-8') as file:
                    try:
                        self.data = json.load(file)
                    except json.JSONDecodeError:
                        self.data = []

    def close_spider(self, spider):
            if self.isBilibili(spider):
                print('end****'*10)
                print(self.data)
                with open(self.file_name, 'w', encoding='utf-8') as file:
                    json.dump(self.data, file, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        if self.isBilibili(spider):
        # print(item)
            self.data.append(item)

            return item
        
        return item