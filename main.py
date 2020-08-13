from multiprocessing import Process
from core.proxy_spider.run_spiders import RunSpider
from core.proxy_test import ProxyTester
from core.proxy_api import ProxyApi


def run():
    process_list = []
    process_list.append(Process(target=RunSpider.start))
    process_list.append(Process(target=ProxyTester.start))
    process_list.append(Process(target=ProxyApi.start))
    for process in process_list:
        process.deamon = True
        process.start()
    for process in process_list:
        process.join()


if __name__ == '__main__':
    run()
