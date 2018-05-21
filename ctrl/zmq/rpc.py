
import asyncio

import zmq

from .base import ZMQClient, ZMQService


class ZMQRPCServer(ZMQService):
    protocol = zmq.REP

    async def handle(self, *args):
        recv = await self.sock.recv_multipart()
        print("MESSAGE RECV: %s" % recv)
        await self.sock.send_multipart(
            [("RECV: %s" % recv).encode('utf-8')])
        asyncio.ensure_future(self.handle())


class ZMQRPCClient(ZMQClient):
    protocol = zmq.REQ

    async def handle(self, command, *args):
        return await getattr(self, "handle_%s" % command)(*args)

    async def handle_stop_service(self, service, *args):
        await self.sock.send_multipart(
            [("stop_service %s" % service).encode("utf-8")])
        print(await self.sock.recv_multipart())
