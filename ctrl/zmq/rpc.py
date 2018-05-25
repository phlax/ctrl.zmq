
import asyncio

from zope import component
from zope import interface
import zope.event
import zope.event.classhandler

import zmq

from .base import ZMQClient, ZMQService
from .events import ZMQRequestEvent, ZMQReplyEvent
from .interfaces import IZMQRPCReply, IZMQRPCServer


@interface.implementer(IZMQRPCServer)
class ZMQRPCServer(ZMQService):
    protocol = zmq.REP

    async def handle(self, *args):
        recv = await self.sock.recv_multipart()
        handler = component.queryAdapter(self, IZMQRPCReply, self.zmqid)
        response = (
            await handler.reply(recv)
            if handler
            else '')
        self.sock.send_multipart([response.encode('utf-8')])
        asyncio.ensure_future(self.handle())


class ZMQRPCClient(ZMQClient):
    protocol = zmq.REQ

    def handle_rpc_request(self, event, uuid=None):
        if event.zmqid == self.zmqid:
            print(
                'RPC Client (%s) sending: %s'
                % (self.zmqid, event.message))
            future_sent = asyncio.ensure_future(
                self.sock.send_multipart(
                    [event.message.encode('utf-8')]))

            def _handle_reply(cb):
                reply = cb.result()
                print('Got response: %s' % reply)
                zope.event.notify(ZMQReplyEvent(self.zmqid, reply, uuid=uuid))

            def _reply(result):
                future_reply = asyncio.ensure_future(
                    self.sock.recv_multipart())
                future_reply.add_done_callback(_handle_reply)
            future_sent.add_done_callback(_reply)

    async def handle(self, *args):
        zope.event.classhandler.handler(
            ZMQRequestEvent,
            self.handle_rpc_request)
