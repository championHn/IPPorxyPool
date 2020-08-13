from core.proxy_spider.base_spider import BaseSpider
import time
import random


class XiciSpider(BaseSpider):
    # 准备URL列表
    urls = ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 11)]
    # 分组的XPATH,用于获取包含代理IP信息的标签列表
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'
    # 组内的XPATH,用于提取IP,port,area
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/a/text()'
    }


class Ip3366Spider(BaseSpider):
    # 准备URL列表
    urls = ['http://www.ip3366.net/free/?stype=1&page={}'.format(i) for i in range(1, 8)]
    # 分组的XPATH,用于获取包含代理IP信息的标签列表
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内的XPATH,用于提取IP,port,area
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }


class KuaiSpider(BaseSpider):
    # 准备URL列表
    urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 6)]
    # 分组的XPATH,用于获取包含代理IP信息的标签列表
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内的XPATH,用于提取IP,port,area
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }

    # 当我们两个页面访问的时间间隔太短,就报错;这是一种反爬手段
    def get_page_from_url(self, url):
        # 随即等待1-3秒
        time.sleep(random.uniform(1, 3))
        # 调用父类方法发送请求获取响应数据
        return super(KuaiSpider, self).get_page_from_url(url)


class Ip66Spider(BaseSpider):
    # 准备URL列表
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 11)]
    # 分组的XPATH,用于获取包含代理IP信息的标签列表
    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'
    # 组内的XPATH,用于提取IP,port,area
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }


if __name__ == '__main__':
    spider = XiciSpider()
    for proxy in spider.get_proxies():
        print(proxy)
    # import requests

    # 测试: http://www.66ip.cn/1.html
    # url = 'http://www.66ip.cn/1.html'
    # resp = requests.get(url)
    # print(resp.status_code)
    # print(resp.content.decode('GBK'))
