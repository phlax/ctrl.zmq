
import asyncio

import zope.event
import zope.event.classhandler

import zmq

from .base import ZMQClient, ZMQService
from .events import ZMQPullEvent, ZMQPushEvent


class ZMQPushServer(ZMQService):
    protocol = zmq.PUSH

    def handle_push(self, event):
        if event.zmqid == self.zmqid:
            asyncio.ensure_future(
                self.sock.send_multipart(
                    [(event.message).encode('utf-8')]))

    async def handle(self, *args):
        zope.event.classhandler.handler(
            ZMQPushEvent,
            self.handle_push)


class ZMQPullClient(ZMQClient):
    protocol = zmq.PULL

    async def handle(self, *args):
        recv = await self.sock.recv_multipart()
        recv = ' '.join(r.decode('utf-8') for r in recv)
        zope.event.notify(ZMQPullEvent(self.zmqid, recv))
        asyncio.ensure_future(self.handle())
