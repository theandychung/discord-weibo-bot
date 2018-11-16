# coding=utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import Base


class Video(Base):
    def __init__(self, id, cache, session):
        super(Video, self).__init__(id, cache, session)

    def _build_url(self):
        pass

