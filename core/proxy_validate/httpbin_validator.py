import time
import requests
import json

from utils.http import get_request_headers
from settings import TEST_TIMEOUT
from utils.log import logger
from domain import Proxy

"""
实现代理池的校验模块
目标: 检查代理IP速度, 匿名程度以及支持的协议类型
步骤:
检查代理IP的速度和匿名程度
    1.代理IP速度: 就是从发送请求到获取响应的时间间隔
    2.匿名程度检查：
        1.对http://httpbin.org/get或https://httpbin.org/get发送请求
        2.如果响应的origin中有','分割的两个IP就是透明代理IP
        3.如果响应的headers中包含Proxy-Connection说明是匿名代理IP,否则就是高匿代理IP
检查代理IP协议类型
    如果http://httpbin.org/get发送请求可以成功, 说明支持http协议
    如果https://httpbin.org/get发送请求可以成功，说明支持https协议
"""


def check_proxy(proxy):
    """
    用于检查指定 代理IP 响应速度,匿名程度,支持协议类型
    :param proxy: 代理IP对象
    :return: 检查后的代理IP模型对象
    """
    # 准备代理IP字典
    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port)
    }
    # 测试该代理IP
    http, http_nick_type, http_speed = __check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies, False)
    # 代理IP支持协议类型, http是0, https是1, https和http都支持是2
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy


def __check_http_proxies(proxies, is_http=True):
    # 代理IP的匿名程度，高匿0, 匿名1, 透明2
    nick_type = -1
    # 响应速度, 单位s
    speed = -1
    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    try:
        # 获取开始时间
        start = time.time()
        # 发送请求,获取响应数据
        response = requests.get(test_url, headers=get_request_headers(), proxies=proxies, timeout=TEST_TIMEOUT)
        if response.ok:
            # 计算响应速度
            speed = round(time.time() - start, 2)
            # 匿名程度
            dic = json.loads(response.text)
            # 获取来源IP:origin
            origin = dic['origin']
            proxy_connection = dic['headers'].get('Proxy-Connection', None)
            # 1.如果响应的origin中有','分割的两个IP就是透明代理IP
            # 代理IP的匿名程度，高匿0, 匿名1, 透明2
            if ',' in origin:
                nick_type = 2
            elif proxy_connection:
                nick_type = 1
            else:
                nick_type = 0

            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as ex:
        logger.exception(ex)
        return False, nick_type, speed


if __name__ == '__main__':
    proxy = Proxy('107.167.207.198', '48678')
    print(check_proxy(proxy))
