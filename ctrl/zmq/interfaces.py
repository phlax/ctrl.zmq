
from zope.interface import Interface


class IZMQRPCServer(Interface):
    pass


class IZMQRPCReply(Interface):

    async def reply(socket, recv):
        pass
