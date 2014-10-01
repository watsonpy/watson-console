# -*- coding: utf-8 -*-
from watson.console import ConsoleError, command
from watson.console.decorators import arg, cmd


class NoCallCommand(command.Base):
    pass


class SampleNonStringCommand(command.Base):
    name = 'nonstring'

    @cmd()
    def execute(self):
        return True


class SampleStringCommand(command.Base):
    name = 'string'

    @cmd()
    def execute(self):
        raise ConsoleError('Something went wrong')


class SampleNoHelpNoExecuteCommand(command.Base):
    name = 'nohelpnoexecute'


class SampleOptionsCommand(command.Base):
    name = 'runoptions'

    @arg('filename', optional=True)
    def execute(self, filename):
        if filename:
            return True
        return None


class SampleArgumentsCommand(command.Base):
    name = 'runargs'

    @cmd()
    def execute(self, argument1, argument2):
        if argument2:
            return True
        return False


class SampleArgumentsWithOptionsCommand(command.Base):
    name = 'runargsoptions'

    @arg('filename', optional=True)
    def execute(self, filename, argument1, argument2):
        if argument1 and filename:
            return True
        return False
