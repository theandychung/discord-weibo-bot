# coding=utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
import math
from ..utils.normal import normal_attr
from ..utils.streaming import streaming
from .base import Base
from ..config.urls import (
    ARTICLE_DETAIL_URL,
    ARTICLE_LIST_URL)


class Article(Base):
    """
    头条文章
    """
    def __init__(self, aid, cache, session):
        super(Article, self).__init__(aid, cache, session)

    def _build_url(self):
        return ARTICLE_DETAIL_URL.format(id=self._id)

    @property
    @streaming()
    def config(self):
        return None

    @property
    @normal_attr(name_in_json='article')
    def content(self):
        """
        文章内容HTML
        :return: 
        """
        return None

    @property
    def title(self):
        """
        文章标题
        :return: 
        """
        return self.config.title

    @property
    def id(self):
        """
        文章ID
        :return: 
        """
        return self.config.id

    @property
    def attitudes_count(self):
        """
        点赞数
        :return: 
        """
        return self.config.attitudes_count

    @property
    def author_name(self):
        """
        文章作者名
        :return: 
        """
        return self.config.author_name

    @property
    def author_uid(self):
        """
        文章作者ID
        :return: 
        """
        return self.config.author_uid

    @property
    def author(self):
        """
        文章作者
        :return: 
        """
        from ..weibo.people import People
        return People(self.author_uid, None, self._session)

    @property
    def image(self):
        """
        头图url
        :return: 
        """
        return self.config.image

    @property
    def read_count(self):
        """
        阅读量
        :return: 
        """
        return self.config.read_count

    @property
    def reposts_count(self):
        """
        转发量
        :return: 
        """
        return self.config.reposts_count


class Articles(Base):
    """
    全部文章
    """

    def __init__(self, uid, cache, session):
        super(Articles, self).__init__(uid, cache, session)
        self._page_num = 1

    def _build_url(self):
        return ARTICLE_LIST_URL.format(id=self._id, page_num=self._page_num)

    @property
    @streaming()
    def data(self):
        return None

    @property
    def _cards(self):
        return self.data.card

    @property
    def _cardlistInfo(self):
        return self.data.cardlistInfo

    @property
    def total(self):
        """
        文章总数
        :return: 
        """
        return self._cardlistInfo.total

    @property
    def _pages(self):
        """
        文章总页数
        :return: 
        """
        return int(math.ceil(self.total / 10))

    def page(self, page_num=1):
        """
        获取某一页的文章，默认只取第一页内容
        :param page_num: 页数 
        :return: 
        """
        from ..weibo.people import People
        from ..weibo.status import Status
        self.refresh()
        self._page_num = page_num
        for card in filter(lambda x: hasattr(x, 'mblog'), self._cards):
            mblog = card.mblog
            # 该article实际也是status，只是在内容中可能会存在文章链接
            # TODO：后期解析出文章内容中的真实文章链接，取出头条文章
            article = Status(mblog.id, None, self._session)
            article.text = mblog.raw_data().get('text')
            article.created_at = mblog.raw_data().get('created_at')
            article.source = mblog.raw_data().get('mblog.source')
            article.thumbnail_pic = mblog.raw_data().get('thumbnail_pic')
            article.bmiddle_pic = mblog.raw_data().get('bmiddle_pic')
            article.original_pic = mblog.raw_data().get('original_pic')
            article.is_paid = mblog.raw_data().get('is_paid')
            article.user = People(mblog.user.id, None, self._session)
            article.pic_urls = [pic.get('url') for pic in mblog.raw_data().get('pics', [])]
            yield article

    def page_from_to(self, from_page, to_page):
        """
        获取从第from_page页到第to_page页的所有文章微博
        :param from_page: int 开始页
        :param to_page: int 结束页
        :return: 
        """
        for page_num in range(from_page, to_page + 1):
            for article in self.page(page_num):
                yield article

    def all(self):
        """
        获取用户的所有文章
        :return: 
        """
        return self.page_from_to(1, self._pages + 1)
