# coding=utf-8
import math

from ..utils.normal import normal_attr
from ..utils.streaming import streaming
from .base import Base
from ..config.urls import (
    STATUS_DETAIL_URL,
    ORI_WEIBO_LIST_URL, WEIBO_LIST_URL)


class Status(Base):
    """
    微博详情
    """

    def __init__(self, aid, cache, session):
        super(Status, self).__init__(aid, cache, session)

    def _build_url(self):
        return STATUS_DETAIL_URL.format(id=self._id)

    @property
    def id(self):
        return self._id

    @property
    @streaming()
    def data(self):
        return None

    @property
    def longTextContent(self):
        return self.data.longTextContent

    @property
    def attitudes_count(self):
        return self.data.attitudes_count

    @property
    def comments_count(self):
        return self.data.comments_count

    @property
    def reposts_count(self):
        return self.data.reposts_count


class Statuses(Base):
    """
    全部微博列表
    """

    def __init__(self, id, cache, session, original=False):
        """
        
        :param id: 
        :param cache: 
        :param session: 
        :param original: 是否原创，默认False 
        """
        super(Statuses, self).__init__(id, cache, session)
        self._page_num = 1
        self._original = original

    def _build_url(self):
        if self._original:
            return ORI_WEIBO_LIST_URL.format(id=self._id, page_num=self._page_num)
        return WEIBO_LIST_URL.format(id=self._id, page_num=self._page_num)

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
    def total(self):
        """微博总数"""
        return self._cardlistInfo.total

    @property
    def _pages(self):
        """微博总页数"""
        return int(math.ceil(self.total/10))

    def page(self, page_num=1):
        """
        获取某一页的微博，默认只取第一页内容
        :param page_num: 页数 
        :return: 
        """
        from ..weibo.people import People
        self.refresh()
        self._page_num = page_num
        for card in filter(lambda x: hasattr(x, 'mblog'), self._cards):
            mblog = card.mblog
            status = Status(mblog.id, None, self._session)
            status.text = mblog.raw_data().get('text')
            status.created_at = mblog.raw_data().get('created_at')
            status.source = mblog.raw_data().get('mblog.source')
            status.thumbnail_pic = mblog.raw_data().get('thumbnail_pic')
            status.bmiddle_pic = mblog.raw_data().get('bmiddle_pic')
            status.original_pic = mblog.raw_data().get('original_pic')
            status.is_paid = mblog.raw_data().get('is_paid')
            status.isTop = mblog.raw_data().get('isTop')
            status.user = People(mblog.user.id, None, self._session)
            status.pic_urls = [pic.get('url') for pic in mblog.raw_data().get('pics', [])]
            yield status

    def page_from_to(self, from_page, to_page):
        """
        获取从第from_page页到第to_page页的所有微博
        :param from_page: 
        :param to_page: 
        :return: 
        """
        for page_num in range(from_page, to_page+1):
            for status in self.page(page_num):
                yield status

    def all(self):
        """
        获取用户的所有微博
        :return: 
        """
        return self.page_from_to(1, self._pages + 1)

