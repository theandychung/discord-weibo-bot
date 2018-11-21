# -*- coding: utf-8 -*-

STR = """
剧场版「Fate/stay night [Heaven's Feel]」的纪念活动即将开启！<br /><br />※关于纪念概念礼装部分，请关注后续官方公告内容。<br /><br />◆活动时间◆<br />2018年11月19日 维护后 ～ 12月3日 13：59<br /><br />为纪念剧场版「Fate/stay night [Heaven's Feel]」，<br />魔术礼装「2004年的碎片」限时登场！<br /><br />◆活动时间◆<br />2018年11月19日 维护后 ～ 12月3日 13：59<br /><br />剧场版「Fate/stay night [Heaven's Feel]」纪念推荐召唤卡池限时开启！<br /><br />◆活动时间◆<br />2018年11月19日 维护后 ～ 12月3日 13：59<br /><br />新从者「★4(SR) 帕尔瓦蒂」登场！<br /><br />此外，「★4(SR) 卫宫（Archer）」「★4(SR) 赫拉克勒斯」「★4(SR) 阿尔托莉雅·潘德拉贡〔Alter〕（Saber）」3骑从者将以每日替换的形式推荐召唤！<br /><br />而包括「★4(SR) 帕尔瓦蒂」在内，「★5(SSR) 阿尔托莉雅·潘德拉贡（Saber）」「★3(R) 库·丘林（Lancer）」「★3(R) 美杜莎（Rider）」「★3(R) 美狄亚」5骑从者将在活动期间全程出现概率提升！<br /><br />※新登场从者「★4(SR) 帕尔瓦蒂」将在推荐召唤结束后，加入剧情卡池。<br /><br />活动期间，限定概念礼装「★5(SSR) 愿之所向」「★4(SR) 战友」「★3(R) 梦之痕迹」全新登场！<br /><br />※活动期间，「★3(R) 梦之痕迹」也可以通过友情召唤获取。<br /><br />「★4(SR) 帕尔瓦蒂」的灵衣全新开放！<br />维护后，将在达芬奇工房内的【魔力棱镜兑换】中，作为新道具，<br />追加「★4(SR) 帕尔瓦蒂」的灵衣开放权！<br /><br />更多活动内容请阅 <a data-url="http://t.cn/E2yRq3f" href="https://game.bilibili.com/fgo/news.html#!news/0/1/2932" data-hide=""><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_web_default.png'></span><span class="surl-text">网页链接</span></a>
"""
# import re
# print(STR)
# m = re.search("(<br\s*\/><br\s*\/>)(?!.*\1).*", STR)
# if m:
#     found = m.group(1)
# print(found)
import re

s_test = """im the first line"""

count =0
sleep_time = 200
import time
while True:
    print(count)
    None if count is 0 else time.sleep(4)
    print("here")
    count = count + 1
