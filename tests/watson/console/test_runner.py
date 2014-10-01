# -*- coding: utf-8 -*-
from pytest import raises
from watson.console import Runner, ConsoleError
from tests.watson.console.support import SampleNonStringCommand


class TestConsoleError(object):

    def test_instance(self):
        exc = ConsoleError()
        assert isinstance(exc, KeyError)


class TestRunner:

    def test_create(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleStringCommand',
            SampleNonStringCommand
        ])
        assert len(runner.commands) == 2

    def test_add_commands(self):
        runner = Runner()
        assert len(runner.commands) == 0
        runner.add_commands(
            [SampleNonStringCommand,
             'tests.watson.console.support.SampleStringCommand'])
        assert len(runner.commands) == 2
        assert not runner.get_command('test')

    def test_no_execute(self):
        with raises(SystemExit):
            runner = Runner(commands=[
                'tests.watson.console.support.SampleNoHelpNoExecuteCommand'
            ])
            runner.execute(['test.py', 'nohelpnoexecute', 'execute'])

    def test_execute_usage(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleStringCommand',
            SampleNonStringCommand
        ])
        with raises(SystemExit):
            runner.execute(['test.py'])  # will print to screen in tests

    def test_execute_command_usage(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleStringCommand',
            SampleNonStringCommand
        ])
        with raises(SystemExit):
            runner.execute(['test.py', 'nonstring', 'execute', '-h'])  # will print to screen in tests

    def test_execute_command_usage_with_args(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleArgumentsCommand'
        ])
        with raises(SystemExit):
            runner.execute(['test.py', 'runargs', 'execute', '-h'])  # will print to screen in tests

    def test_execute_command_usage_with_options(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleOptionsCommand'
        ])
        with raises(SystemExit):
            runner.execute(['test.py', 'runoptions', 'execute', '-h'])  # will print to screen in tests

    def test_execute_command_with_options_invalid(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleOptionsCommand'
        ])
        with raises(SystemExit):
            runner.execute(['test.py', 'runoptions', 'execute', '-d'])  # will print to screen in tests

    def test_execute_command_with_error(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleStringCommand'
        ])
        with raises(SystemExit):
            runner(['test.py', 'string', 'execute'])

    def test_execute_command(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleNonStringCommand'
        ])
        assert runner(['test.py', 'nonstring', 'execute'])

    def test_execute_command_with_options(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleOptionsCommand'
        ])
        output = runner.execute(['test.py', 'runoptions', 'execute', '--filename', 'test'])  # will print to screen in tests
        assert output

    def test_execute_command_with_args(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleArgumentsCommand'
        ])
        output = runner.execute(['test.py', 'runargs', 'execute', 'test', 'test2'])  # will print to screen in tests
        assert output

    def test_execute_command_with_args_options(self):
        runner = Runner(commands=[
            'tests.watson.console.support.SampleArgumentsCommand',
            'tests.watson.console.support.SampleArgumentsWithOptionsCommand'
        ])
        output = runner.execute(['test.py', 'runargsoptions', 'execute', 'arg1', 'arg2', '--filename', 'filename.txt'])  # will print to screen in tests
        assert output
