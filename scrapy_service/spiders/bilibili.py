import scrapy
import time
from scrapy_service.items  import BilibiliItem
from tqdm import tqdm
class BilibiliSpider(scrapy.Spider):
    name = "b"
    allowed_domains = ["search.bilibili.com"]

    keyWords = [
    "人工智能",
    "机器学习",
    "word2vec"
]


  

    def start_requests(self):
        for item in  tqdm(self.keyWords):
            url = f"https://search.bilibili.com/all?keyword={item}&search_source=1"
            print(url)
            yield scrapy.Request(url=url, callback=self.parse,meta={"keyword":item})

    def parse(self, response):
   
        datas=response.xpath("//div[@class='bili-video-card']")
 
        result=[]
        for data in datas:
            item=BilibiliItem()
            item["title"]=data.xpath(".//div[@class='bili-video-card__info--right']//h3/@title").get()
            item["url"]='https:' +data.xpath(".//div[@class='bili-video-card__info--right']/a/@href").get()
            result.append(dict(item))
     

        yield {
            "keyWord":response.meta["keyword"],
            "list":result
        }
      
