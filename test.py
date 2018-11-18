#!coding=utf-8
import requests
import re
import pandas as pd


def get_proxy():
    """
    获取代理
    """
    # 获取xicidaili的高匿代理
    ##proxy_info_list = []  # 抓取到的ip列表
    ip_list = []
    dk_list = []
    xy_list = []
    ip_list1 = []
    dk_list1 = []
    xy_list1 = []
    for page in range(1, 2):  # 抓几页
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}

        request = requests.get('http://www.xicidaili.com/nn/%d' % page, headers=headers, verify=False)
        r = request.text

        ip_page = re.findall(r'<td>(.*?)</td>', r)
        # print (ip_page)

        for i in range(0, len(ip_page), 5):
            ip_list.append(ip_page[i])
            dk_list.append(ip_page[i + 1])
            xy_list.append(ip_page[i + 2])

    # 随机选择
    # ran=random.randint(1, len(ip_list))
    # ip=ip_list[ran]+':'+dk_list[ran]
    # xy=str(xy_list[ran]).lower()

    # print (xy + ip)

    """
      # 验证代理的可用性
    """

    for i in range(0, len(ip_list)):  #
        if xy_list[i] == 'HTTP':
            try:
                proxies = {'http': ip_list[i] + ':' + dk_list[i]}  # http 一定要小写
                url = 'http://checkip.amazonaws.com/'
                testip = requests.get(url=url, proxies=proxies, headers=headers, timeout=3, verify=False)
                regetip = testip.text.strip()

                if regetip == ip_list[i]:
                    ip_list1.append(ip_list[i])
                    dk_list1.append(dk_list[i])
                    xy_list1.append(xy_list[i])
            except:
                print(i)
    df = pd.DataFrame()
    df.loc[:, 'xy'] = xy_list1
    df.loc[:, "ip"] = ip_list1
    df.loc[:, 'dk'] = dk_list1

    df.to_csv(r'E:\daili.csv', index=False, encoding="GB18030")
    print(df)
    return df


get_proxy()

