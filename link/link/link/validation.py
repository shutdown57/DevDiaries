import re
from urllib.parse import urlparse

from link.models import Link, Tag


class LinkValidation:
    NAME = r'([a-zA-Z0-9]){3,}'
    DESCRIPTION = r'(.*)'
    ACTIVE = r'([1-2]){1}'
    WEB_IMG = r'(.*)'

    @classmethod
    def form(cls, data):
        if not data:
            return False
        if not cls.name(data['name']):
            return False
        if not cls.active(data['active']):
            return False
        if not cls.description(data['description']):
            return False
        if not cls.web_img(data['web_img']):
            return False
        return True

    @classmethod
    def name(cls, name_):
        return bool(re.match(cls.NAME, name_))

    @classmethod
    def description(cls, description_):
        return bool(re.match(cls.DESCRIPTION, description_))

    @classmethod
    def active(cls, active_):
        return bool(re.match(cls.ACTIVE, active_))

    @classmethod
    def web_img(cls, web_img_):
        return bool(re.match(cls.WEB_IMG, web_img_))
