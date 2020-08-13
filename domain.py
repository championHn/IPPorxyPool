from settings import MAX_SCORE

"""
定义代理IP的数据模型
目标：定义代理IP的数据模型类
步骤：
1.定义Proxy类,继承object
2.实现__init__方法,负责初始化,包含如下字段:
    IP:代理IP地址
    port:代理IP的端口号
    protocol: 代理IP支持协议类型,http是0,https是1,https和http都支持是2
    nick_type: 代理IP的匿名程度，高匿0,匿名1,透明2
    speed: 代理IP的响应速度,单位s
    area: 代理IP的所在地区
    score: 代理IP评分，用于衡量代理的可能性;默认分值可以通过配置文件进行配置,在进行代理可用性检查的时候,
            没遇到一次请求失败就减1分,减到0的时候从池中删除,如果检查代理可用,就恢复默认值
    disable_domains: 不可用域名列表,有些代理IP在某些域名下不可用,但是在其他域名下可用
    在配置文件: settings.py 中定义MAX_SCORE = 50,表示代理IP的默认分数
3.提供__str__方法, 返回数据字符串
"""


class Proxy(object):
    def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE, disable_domains=[]):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.nick_type = nick_type
        self.speed = speed
        self.area = area
        self.score = score
        self.disable_domains = disable_domains

    def __str__(self):
        return str(self.__dict__)
