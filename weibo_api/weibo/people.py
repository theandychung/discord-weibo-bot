# coding=utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
import math

from ..utils.streaming import streaming
from .base import Base
from ..config.urls import (
    PEOPLE_DETAIL_URL,
    FOLLOWS_LIST_URL,
    FOLLOWERS_LIST_URL,
)


class People(Base):
    def __init__(self, uid, cache, session):
        super(People, self).__init__(uid, cache, session)

    def _build_url(self):
        return PEOPLE_DETAIL_URL.format(id=self._id)

    @property
    @streaming()
    def data(self):
        return None

    @property
    def userInfo(self):
        return self.data.userInfo

    @property
    def id(self):
        """
        用户ID
        """
        return self.userInfo.id

    @property
    def name(self):
        """
        昵称
        """
        return self.userInfo.screen_name

    @property
    def description(self):
        """
        用户概述
        """
        return self.userInfo.description

    @property
    def gender(self):
        """
        性别
        """
        return self.userInfo.gender

    @property
    def avatar(self):
        """
        头像图片URL
        :return: 
        """
        return self.userInfo.avatar_hd

    @property
    def followers_count(self):
        """
        他的粉丝数
        :return: 
        """
        return self.userInfo.followers_count

    @property
    def follow_count(self):
        """
        他关注的用户数量
        :return: 
        """
        return self.userInfo.follow_count

    @property
    def followers(self):
        """
        该用户的粉丝
        :return: 
        """
        return Peoples(self._id, None, self._session, utype='follower')

    @property
    def follows(self):
        """
        他关注的用户
        :return: 
        """
        return Peoples(self._id, None, self._session, utype='follow')

    @property
    def statuses(self):
        """
        他的微博动态
        :return: 
        """
        from ..weibo.status import Statuses
        return Statuses(self._id, None, self._session)

    @property
    def origin_statuses(self):
        """
        他的原创微博
        :return: 
        """
        from ..weibo.status import Statuses
        return Statuses(self._id, None, self._session, original=True)

    @property
    def articles(self):
        """
        他的文章
        :return: 
        """
        from ..weibo.article import Articles
        return Articles(self._id, None, self._session)


class Peoples(Base):
    def __init__(self, uid, cache, session, utype='follower'):
        """
        粉丝或关注的用户
        :param uid: 
        :param cache: 
        :param session: 
        :param utype: 用户类型，follower表示他的粉丝，follow表示他关注的用户
        """
        super(Peoples, self).__init__(uid, cache, session)
        self._page_num = 1
        self._utype = utype

    def _build_url(self):
        if self._utype == 'follow':
            return FOLLOWS_LIST_URL.format(id=self._id, page_num=self._page_num)
        return FOLLOWERS_LIST_URL.format(id=self._id, page_num=self._page_num)

    @property
    @streaming()
    def data(self):
        return None

    @property
    def _cards(self):
        return self.data.cards

    @property
    def _cardlistInfo(self):
        return self.data.cardlistInfo

    @property
    def _card_group(self):
        """
        带title的card的card_group
        :return: 
        """
        return list(filter(lambda x: not hasattr(x, 'card_style'), self._cards))[0].card_group

    @property
    def total(self):
        """
        粉丝or关注总数
        :return: 
        """
        p = People(self._id, None, self._session)
        peoples_num = p.followers_count if self._utype == "follower" else p.follow_count
        return peoples_num

    @property
    def _pages(self):
        """
        粉丝or关注总页数
        :return: 
        """
        return int(math.ceil(self.total / 20))  # 每页显示20个粉丝or关注的用户

    def page(self, page_num=1):
        """
        获取某一页的粉丝，默认第一页，每页20条记录
        :param page_num: 
        :return: 
        """
        self.refresh()
        self._page_num = page_num
        for card in list(filter(lambda x: hasattr(x, 'user'), self._card_group)):
            cache = {'userInfo': card.user.raw_data()}
            fan = People(card.user.id, cache, self._session)
            yield fan

    def page_from_to(self, from_page, to_page):
        """
        获取从第 from_page 页 到第 to_page 页的粉丝 or 关注的用户
        :param from_page: 
        :param to_page: 
        :return: 
        """
        for page_num in range(from_page, to_page + 1):
            for fan in self.page(page_num):
                yield fan

    def all(self):
        """
        获取他的所有粉丝列表，目前看来API只允许获取250页粉丝(5000个)
        or 获取他的所有关注的用户，限制显示10页他关注的用户(200个)
        :return: 
        """
        if self._utype == 'follow':
            return self.page_from_to(1, self._pages + 1) if self._pages < 10 else self.page_from_to(1, 10)
        return self.page_from_to(1, self._pages + 1) if self._pages < 250 else self.page_from_to(1, 250)
