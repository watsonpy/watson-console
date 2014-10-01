# -*- coding: utf-8 -*-
import abc
import sys
from watson.common import strings
from watson.common.contextmanagers import suppress


class Base(metaclass=abc.ABCMeta):
    """The base command that outlines the required structure for a console
    command.

    Help is automatically invoked when the `-h` or `--help` option is used
    or when the command or namespace is not specified.

    If a name attribute is not specified on the class then a snake_cased
    version of the name will be used in its place.

    http://docs.python.org/dev/library/argparse.html#the-add-argument-method

    Example:

    .. code-block:: python

        # can be executed by `script.py my_namespace command`
        class MyNamespace(command.Base, ContainerAware):
            help = 'Top level namespace message'

            @arg()
            def command(self):
                '''Command specific help.
                '''
                print('Run!')

        # with arguments from the function
        # can be executed by `script.py my_namespace command somevalue
        class MyNamespace(command.Base, ContainerAware):
            help = 'Top level namespace message'

            @arg()
            def command(self, value):
                '''Command specific help.

                Args:
                    value: A value to pass
                '''
                print('Run', value)

        # with options
        class MyNamespace(command.Base, ContainerAware):
            help = 'Top level namespace message'

            @arg('value', optional=True)
            def command(self, value):
                '''Command specific help.
                '''
                print('Run!')
    """
    name = None

    @classmethod
    def help(cls):
        if not cls.__doc__:
            cls.__doc__ = 'Missing help.'
        return cls.__doc__.splitlines()[0]

    @classmethod
    def cased_name(cls):
        if not cls.name:
            cls.name = cls.__name__
        return strings.snakecase(cls.name)

    def write(self, message=None, error=False):
        out = sys.stderr if error else sys.stdout
        if not message:
            message = ''
        out.write(message + '\n')


def find_commands_in_module(module):
    """Retrieves a list of all commands within a module.

    Returns:
        A list of commands from the module.
    """
    commands = []
    for key in dir(module):
        item = getattr(module, key)
        with suppress(Exception):
            if issubclass(item, Base) and item != Base:
                commands.append(item)
    return commands
