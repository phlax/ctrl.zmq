
import asyncio

import zmq

import zope.event
import zope.event.classhandler

from .base import ZMQClient, ZMQService
from .events import ZMQSubscriberEvent, ZMQPublisherEvent


class ZMQSubscriber(ZMQService):
    protocol = zmq.SUB

    async def run(self, subscribe, *args):
        self.sock.setsockopt_string(zmq.SUBSCRIBE, subscribe)
        asyncio.ensure_future(self.handle())
        return 'Subscribed %s (%s)' % (subscribe, self)

    async def handle(self, *args):
        recv = await self.sock.recv_multipart()
        subscription = recv[0].split()[0]
        msg = ' '.join(recv[0].decode('utf-8').split()[1:])
        zope.event.notify(ZMQSubscriberEvent(self.zmqid, subscription, msg))
        asyncio.ensure_future(self.handle())


class ZMQPublisher(ZMQClient):
    protocol = zmq.PUB
    wait_on_start = .1

    def handle_publish(self, event):
        if event.zmqid == self.zmqid:
            asyncio.ensure_future(
                self.sock.send_multipart([event.payload]))

    async def handle(self, *args):
        zope.event.classhandler.handler(
            ZMQPublisherEvent,
            self.handle_publish)
