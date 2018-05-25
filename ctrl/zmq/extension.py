
from zope import component

from ctrl.core.interfaces import ICommandRunner, ISubcommand

from .command import ZMQSubcommand


class CtrlZMQExtension(object):

    @property
    def requires(self):
        return ['config', 'command']

    async def register(self, app):
        component.provideAdapter(
            factory=ZMQSubcommand,
            adapts=[ICommandRunner],
            provides=ISubcommand,
            name='zmq')
