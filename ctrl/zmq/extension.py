
from zope import component

from ctrl.core.extension import CtrlExtension
from ctrl.core.interfaces import (
    ICommandRunner, ICtrlExtension, ISubcommand)

from .command import ZMQSubcommand


class CtrlZMQExtension(CtrlExtension):

    @property
    def requires(self):
        return ['config', 'command']

    def register_adapters(self):
        component.provideAdapter(
            factory=ZMQSubcommand,
            adapts=[ICommandRunner],
            provides=ISubcommand,
            name='zmq')


# register the extension
component.provideUtility(
    CtrlZMQExtension(),
    ICtrlExtension,
    'zmq')
