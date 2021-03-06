# Tai Sakuma <tai.sakuma@gmail.com>
from ..roottree import BEventBuilder as BaseEventBuilder

##__________________________________________________________________||
class EventBuilder(object):
    def __init__(self, config):
        self.baseBuilder = BaseEventBuilder(config)
        self.config = config

    def __repr__(self):
        return '{}(baseBuilder={!r}, config={!r})'.format(
            self.__class__.__name__,
            self.baseBuilder,
            self.config
        )

    def __call__(self):
        events = self.baseBuilder()
        return events

##__________________________________________________________________||
