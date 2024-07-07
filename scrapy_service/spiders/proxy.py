import scrapy
from scrapy_service.items import ProxyPoolItem
import re
import json


class ExampleSpider(scrapy.Spider):
    name = "proxy_spider"
    allowed_domains = ["kuaidaili.com"]
    # start_urls = ["https://www.kuaidaili.com/free/"]
    start_urls = ["https://www.kuaidaili.com/free/dps/"]

    def __init__(self):
        # super().__init__(name, **kwargs)

        # for i in range(1, 4):
        #     self.start_urls.append(f"https://www.kuaidaili.com/free/inha/{i}/")
        # print(self.start_urls)
        pass
  

    def parse(self, response):
        # print(response.text)
        # 正则获取js中 const fpsList = []
       
        res=re.search(r'const fpsList = (.*?);',response.text).group(1)
        print(res)
        # print(type(res))
        tableList = json.loads(res)

# 打印解析后的列表
        print(tableList)
        print('***'*20)
        # tableList=eval(res)
       
        # with open('proxies.txt', 'a') as f:
        #     for proxy in tableList:   
        #         f.write(f"{proxy["ip"]}:{proxy["port"]}\n")

        for i in tableList:
            print(i)
            yield {
                "proxy":f"{i['ip']}:{i['port']}"
            }            





        # response.xpath("//title/text()").extract_first()
        # 获取tbody.kdl-table-tbody下的所有tr标签
        # print(response.text)
        # print('***'*20)
        # trs = response.xpath("//tbody[@class='kdl-table-tbody']/tr")
        # for tr in trs:
        #     # 获取tr标签下的td标签
        #     item=ProxyPoolItem()

        #     tds = tr.xpath("./td")
        #     item['ip'] = tds[0].xpath("./text()").extract_first()
        #     item['port'] = tds[1].xpath("./text()").extract_first()
        #     # print(ip, port)
        #     # print(dict(item))
        #      # 将代理 IP 存储到文件或其他地方
           
