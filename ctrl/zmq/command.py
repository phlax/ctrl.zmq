
from zope import interface

from ctrl.core.interfaces import ISubcommand

from .pubsub import ZMQPublisher
from .rpc import ZMQRPCClient


@interface.implementer(ISubcommand)
class ZMQSubcommand(object):

    def __init__(self, context):
        self.context = context

    async def handle(self, loop, command, *args):
        return await getattr(self, 'handle_%s' % command)(loop, *args)

    async def handle_rpc(self, loop, server_addr, command, *args):
        client = ZMQRPCClient(loop, server_addr)
        return await client.handle(command, *args)

    async def handle_publish(self, loop, server_addr, command, *args):
        client = ZMQPublisher(loop, server_addr)
        return await client.handle(command, *args)
