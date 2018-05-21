
import asyncio

import zmq

from .base import ZMQClient, ZMQService


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
        print("Received (%s): %s" % (subscription, msg))
        asyncio.ensure_future(self.handle())


class ZMQPublisher(ZMQClient):
    protocol = zmq.PUB
    wait_on_start = .1

    async def handle_service_stopped(self, subscription, service, *args):
        await self.sock.send_multipart(
            [("%s service_stopped %s"
              % (subscription, service)).encode("utf-8")])
        return (
            'Published service_stopped %s %s/%s'
            % (service, self.server_addr,  subscription))
