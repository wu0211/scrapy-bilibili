# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import base64
from scrapy import signals
from scrapy.http import HtmlResponse
import time
from scrapy.exceptions import NotConfigured
from selenium import webdriver
# useful for handling different item types with a single interface
from scrapy_service.settings import USER_AGENT_LIST
import os


# 定义一个中间件类
class RandomUserAgentMiddleware:
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = user_agent



class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(spider.settings.get("PROXY_LIST"))

        if "user_passwd" in proxy:
            request.meta["proxy"] = f"http://{proxy['ip_port']}"
            encoded_user_pass = base64.b64encode(proxy['user_passwd'].encode()).decode()
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        else:
            request.meta["proxy"] = f"http://{proxy['ip_port']}"

class BiliBiliSeleniumMiddleware(object):

    def process_request(self, request, spider):
        url=request.url
        if spider.name=="b":

            # 获取settings 文件配置
            settings=spider.settings
            # 获取配置的浏览器
            chromedriverPath=settings.get("CHROME_DRIVER_PATH")
            
            if not os.path.exists(chromedriverPath):
                raise NotConfigured("请配置chrome驱动路径")

            service = webdriver.ChromeService(executable_path=chromedriverPath)
            options=webdriver.ChromeOptions()
            options.add_argument("--headless")
            driver=webdriver.Chrome(service=service,options=options)
       
            driver.get(url)
            # 等待10秒
            time.sleep(1) 
            data=driver.page_source
            driver.close()

            return HtmlResponse(url=url,body=data,encoding="utf-8",request=request)


    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls()
