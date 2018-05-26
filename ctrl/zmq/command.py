
import os

from zope import interface
from zope.dottedname.resolve import resolve

from ctrl.core.constants import RUN_FOREVER
from ctrl.core.interfaces import ISubcommand

from .pubsub import ZMQPublisher
from .rpc import ZMQRPCClient


class ZMQUpCommand(object):

    @property
    def apps(self):
        return [
            (k[8:], v.split(' ')[0], v.split(' ')[1:])
            for k, v
            in os.environ.items()
            if k.startswith('ZMQ_APP')]

    @property
    def router(self):
        if 'ZMQ_ROUTER' in os.environ:
            router = os.environ['ZMQ_ROUTER'].split(' ')
            return router[0], router[1:]

    async def handle(self, *args, loop=None):
        if self.router:
            await resolve(self.router[0])().route(*self.router[1])
        for k, app, args in self.apps:
            handler = resolve(app)(k, args[0], loop=loop)
            response = await handler.run(*args[1:])
            if response is not None:
                print(response)
        return RUN_FOREVER


@interface.implementer(ISubcommand)
class ZMQSubcommand(object):

    def __init__(self, context):
        self.context = context

    async def handle(self, command, *args, loop=None):
        return await getattr(self, 'handle_%s' % command)(*args, loop=loop)

    async def handle_rpc(self, server_addr, command, *args, loop=None):
        client = ZMQRPCClient(loop, server_addr)
        return await client.handle(command, *args)

    async def handle_publish(self, server_addr, command, *args, loop=None):
        client = ZMQPublisher(loop, server_addr)
        return await client.handle(command, *args)

    async def handle_up(self, *args, loop=None):
        return await ZMQUpCommand().handle(*args)
