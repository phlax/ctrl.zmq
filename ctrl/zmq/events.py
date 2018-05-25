

class ZMQEvent(object):

    def __init__(self, zmqid, message):
        self.zmqid = zmqid
        self.message = message

    def __repr__(self):
        return self.__class__.__name__

    @property
    def payload(self):
        return self.message.encode('utf-8')


class ZMQRequestEvent(ZMQEvent):
    pass


class ZMQReplyEvent(ZMQEvent):

    def __init__(self, zmqid, message, uuid=None):
        self.zmqid = zmqid
        self.message = message
        self.uuid = uuid


class ZMQPushEvent(ZMQEvent):
    pass


class ZMQPullEvent(ZMQEvent):
    pass


class ZMQSubscriberEvent(ZMQEvent):

    def __init__(self, zmqid, subscription, message):
        self.zmqid = zmqid
        self.subscription = subscription
        self.message = message


class ZMQPublisherEvent(ZMQEvent):

    def __init__(self, zmqid, subscription, message):
        self.zmqid = zmqid
        self.subscription = subscription
        self.message = message

    @property
    def payload(self):
        return (
            "%s %s"
            % (self.subscription,
               self.message)).encode('utf-8')
