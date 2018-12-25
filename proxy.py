#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


class SingleIP:
    def __init__(self, protocol, ip, port, ping):
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.ping = ping

    def __repr__(self):
        return self.protocol + '://' + self.ip + ':' + self.port


class IPPool:
    def __init__(self):
        self.ip_list = self.import_ip()

    def import_ip(self):
        ip_list = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        url = 'https://www.kuaidaili.com/free/intr/'
        try:
            web_data = requests.get(url, headers=headers)
        except ConnectionError:
            print("cannot get IPs from kuaidaili")
            return None

        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            protocol = tds[3].text.lower()
            ip = tds[0].text
            port = tds[1].text
            try:
                requests.get('https://m.weibo.cn/', proxies={protocol: ip+':'+port})
                ip_list.append(SingleIP(protocol=protocol,
                                        ip=ip,
                                        port=port,
                                        ping=float(tds[5].text[:-1])))
            except:
                pass
        ip_list = sorted(ip_list, key=lambda x: float(x.ping))
        return ip_list

    def next_ip(self):
        if self.is_empty() is False:
            print("getting new ip from storage")
            ip = self.ip_list[0]
            del self.ip_list[0]
            return ip
        else:
            print("getting new list")
            self.ip_list = self.import_ip()

    def is_empty(self):
        if not self.ip_list:
            return True
        return False


if __name__ == '__main__':
    pool = IPPool()
    print(''.join(repr(pool.ip_list)))
    print(pool.next_ip())
