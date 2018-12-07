from jinja2 import Markup
from datetime import datetime


class Moment:
    """
    Convert timestamp to human readable datetime
    :param timestamp_ int: time stamp
    """
    def __init__(self, timestamp_):
        self.timestamp = timestamp_

    def render(self, format_):
        """
        Render time stamp to given format and functisons
        :param format_ str: support momentjs format style to render
        :return Markup: return markup string
        """
        return Markup(
            "<script>document.write(moment.unix({date}).{fmt})</script>"
        ).format(date=self.timestamp, fmt=format_)

    def format(self, fmt):
        """
        Use render method to render time stamp with given format
        :param fmt str: format style from momentjs library
        :return Markup: return markup string
        """
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        """
        Use calendar method of momentjs library
        :return Markup: return markup string
        """
        return self.render("calendar()")

    def from_now(self):
        """
        Use fromNow method of momentjs library
        :return Markup: return markup string
        """
        return self.render("fromNow()")
