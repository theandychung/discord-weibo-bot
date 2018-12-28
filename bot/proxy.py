#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


class IPPool:
    def __init__(self):
        pass

    @property
    def get_sslproxies_ip(self):
        proxy_ip = {}
        url = 'https://www.sslproxies.org/'
        try:
            web_data = requests.get(url)
        except ConnectionError:
            print("cannot get IPs from sslproxies")
            return None
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        # for i in range(1, min(len(ips), 5)):
        for i in range(1, len(ips[1:100])):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            protocol = 'https'
            ip = tds[0].text
            port = tds[1].text
            try:
                requests.get('https://m.weibo.cn/',
                             proxies={protocol: protocol + '://' + ip + ':' + port},
                             timeout=3)
                proxy_ip = {protocol: protocol + '://' + ip + ':' + port}
                print(proxy_ip)
                break
            except:
                pass
        if proxy_ip == {}:
            import time
            print("did not find any good ip, wait 360 sec for a new list")
            time.sleep(360)
            proxy_ip = self.get_sslproxies_ip()
        return proxy_ip



if __name__ == '__main__':
    # proxy = IPPool().get_sslproxies_ip
    # print(proxy)

    proxy = {'https': 'https://66.98.56.237:8080'}
    print(requests.get("https://httpbin.org/ip", proxies=proxy).text)
    print(requests.get('https://m.weibo.cn/', proxies=proxy).status_code)


    # def get_tor_session():
    #     session = requests.session()
    #     session.proxies = {'https': 'https://87.247.24.198:59546'}
    #     return session
    # session = get_tor_session()
    # session.get("https://m.weibo.cn/")
    # print(session.get("https://httpbin.org/ip").text)
    # Above should print an IP different than your public IP

    # Following prints your normal public IP
    # print(requests.get("https://httpbin.org/ip").text)
