# coding=utf-8
from __future__ import unicode_literals
from __future__ import print_function
import requests

__all__ = ['WeiboClient']


class WeiboClient(object):
    def __init__(self):
        self._session = requests.session()

    def people(self, uid):
        """
        用户相关信息
        :param uid: 
        :return: 
        """
        from .weibo.people import People
        return People(uid, None, self._session)

    def status(self, sid):
        """
        微博详情
        :param sid: 
        :return: 
        """
        from .weibo.status import Status
        return Status(sid, None, self._session)

    def statuses(self, uid):
        """
        全部微博列表
        :param uid: 
        :return: 
        """
        from .weibo.status import Statuses
        return Statuses(uid, None, self._session)

    def origin_statuses(self, uid):
        """
        原创微博列表
        :param uid: 
        :return: 
        """
        from .weibo.status import Statuses
        return Statuses(uid, None, self._session, original=True)

    def article(self, aid):
        """
        文章相关信息
        :param aid: 
        :return: 
        """
        from .weibo.article import Article
        return Article(aid, None, self._session)

    def articles(self, uid):
        """
        文章列表
        :param uid: 
        :return: 
        """
        from .weibo.article import Articles
        return Articles(uid, None, self._session)

    def origin_articles(self, uid):
        """
        原创文章列表
        :param uid: 
        :return: 
        """
        pass

    def followers(self, uid):
        """
        粉丝列表
        :param uid: 
        :return: 
        """
        from .weibo.people import Peoples
        return Peoples(uid, None, self._session, utype='follower')

    def follow(self, uid):
        """
        关注列表
        :param uid: 
        :return: 
        """
        from .weibo.people import Peoples
        return Peoples(uid, None, self._session, utype='follow')
